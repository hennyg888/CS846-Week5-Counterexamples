# Architecture Overview 🔧

## Purpose
A concise, high-level description of the package layout and the runtime pipeline.

## Layers
- **Backend (primitives & cache)** — low-level hashing, bit-twiddling, and a tiny key-value cache.
- **Midend (compositions & engines)** — composes backend primitives into higher-level transforms and internal engines.
- **Frontend (runners & shims)** — thin wrappers that call the midend and present outputs.

## Data Flow
Frontends call midend functions (e.g., `snorfle`, `quibble`, `obscure_chain`), which in turn call backend primitives (e.g., `tangle`, `flux`, `sift_kit`) to produce integers, sequences, or tokens. The `secret_cache` provides a tiny, in-process stash used by some midend functions.

## Key properties
- Deterministic, pure-ish transforms (no external I/O except `print` in frontends).
- Intentional obfuscation in naming but clear functional layering.
- Lightweight import-time hacks (manipulating `sys.path`) used by frontend scripts.
