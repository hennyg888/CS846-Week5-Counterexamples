'''
The code was taken from HuggingFace repository. The summaries for classes were removed.
Link: https://github.com/huggingface/transformers/blob/main/src/transformers/models/aria/modeling_aria.py
'''


from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional

import torch
from torch import nn

from ... import initialization as init
from ...activations import ACT2FN
from ...cache_utils import Cache, DynamicCache
from ...generation import GenerationMixin
from ...integrations import use_kernel_forward_from_hub, use_kernel_func_from_hub, use_kernelized_func
from ...masking_utils import create_causal_mask
from ...modeling_flash_attention_utils import FlashAttentionKwargs
from ...modeling_layers import GradientCheckpointingLayer
from ...modeling_outputs import (
    BaseModelOutputWithPast,
    BaseModelOutputWithPooling,
    CausalLMOutputWithPast,
    ModelOutput,
)
from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS, dynamic_rope_update
from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel
from ...processing_utils import Unpack
from ...utils import TransformersKwargs, auto_docstring, can_return_tuple, torch_compilable_check
from ...utils.generic import check_model_inputs, maybe_autocast, merge_with_config_defaults
from ..auto import AutoModel
from .configuration_aria import AriaConfig, AriaTextConfig

class AriaProjector(nn.Module):

    def __init__(
        self,
        config: AriaConfig,
    ):
        super().__init__()

        self.patch_to_query_dict = config.projector_patch_to_query_dict
        self.in_features = config.vision_config.hidden_size
        self.num_heads = config.vision_config.num_attention_heads
        self.kv_dim = config.vision_config.hidden_size
        self.hidden_features = config.text_config.hidden_size
        self.output_dim = config.text_config.hidden_size

        self.query = nn.Parameter(torch.zeros(config.max_value_projector_patch_to_query_dict, self.in_features))

        self.cross_attn = AriaCrossAttention(config)

        self.layer_norm = nn.LayerNorm(self.in_features)
        self.feed_forward = AriaProjectorMLP(self.in_features, self.hidden_features, self.output_dim)

    def forward(self, key_value_states: torch.Tensor, attn_mask: torch.Tensor | None = None):
       
        batch_size, num_patches = key_value_states.shape[0], key_value_states.shape[1]

        if num_patches not in self.patch_to_query_dict:
            raise KeyError(
                f"Number of patches {num_patches} not found in patch_to_query_dict amongst possible values {self.patch_to_query_dict.keys()}."
            )
        query_num = self.patch_to_query_dict[num_patches]

        queries = self.query[:query_num].unsqueeze(0).repeat(batch_size, 1, 1)

        if attn_mask is not None:
            attn_mask = attn_mask.repeat_interleave(self.num_heads, 0)
            attn_mask = attn_mask.unsqueeze(1).expand(-1, queries.size(1), -1)

        attention_out = self.cross_attn(key_value_states, queries, attn_mask=attn_mask)

        out = self.feed_forward(self.layer_norm(attention_out))

        return out


class AriaSharedExpertsMLP(nn.Module):

    def __init__(self, config: AriaTextConfig):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        self.intermediate_size = config.intermediate_size * config.moe_num_shared_experts
        self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=config.mlp_bias)
        self.up_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=config.mlp_bias)
        self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size, bias=config.mlp_bias)
        self.act_fn = ACT2FN[config.hidden_act]

    def forward(self, x):
        down_proj = self.down_proj(self.act_fn(self.gate_proj(x)) * self.up_proj(x))
        return down_proj


def sequential_experts_gemm(token_states, expert_weights, tokens_per_expert):
  
    num_tokens = token_states.shape[0]
    out_features = expert_weights.shape[-1]
    output = torch.zeros(num_tokens, out_features, dtype=token_states.dtype, device=token_states.device)

    cumsum_num_tokens = torch.cumsum(tokens_per_expert, dim=0)
    # Insert zero at the beginning for offset index's convenience
    zero_tensor = torch.zeros(1, dtype=torch.long, device=cumsum_num_tokens.device)
    cumsum_num_tokens = torch.cat((zero_tensor, cumsum_num_tokens))

    for expert_num in range(expert_weights.shape[0]):
        start = cumsum_num_tokens[expert_num]
        end = cumsum_num_tokens[expert_num + 1]
        tokens = token_states[start:end]

        out = torch.matmul(tokens, expert_weights[expert_num])
        output[start:end] = out
    return output


class AriaGroupedExpertsGemm(nn.Module):

    def __init__(self, in_features, out_features, groups):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.groups = groups
        self.weight = nn.Parameter(torch.empty(groups, in_features, out_features))

    def forward(self, input, tokens_per_expert):
        """
        Perform grouped matrix multiplication.

        Args:
            input (`torch.Tensor`):
                Input tensor of shape (num_tokens, in_features).
            tokens_per_expert (`torch.Tensor`):
                Number of tokens assigned to each expert.

        Returns:
            torch.Tensor: Output tensor of shape (num_tokens, out_features).
        """
        return sequential_experts_gemm(
            input,
            self.weight,
            tokens_per_expert.cpu(),
        )