# Backend Primitives & Cache 🔐

## Core transforms (`backend_processing/core_back.py`)
- `tangle(src, twist=0x5A)` — MD5-based integer conversion and bit mixing.
- `flux(n, mask=0xDEADBEEF)` — 32-bit rotate and xor mask for integer mixing.
- `sift_kit(data, key=None)` — small checksum-like scalar from bytes and optional key.

## Arcane utilities (`backend_processing/arcane_tools.py`)
- `warp(x, salt=...)` — string-to-sum bit-shift transformation.
- `sieve(seq)` — maps sequence elements to small ints using enumerate and bit ops.
- `churn(a, b)` — multiplicative mix of two ints.

## Cache (`backend_processing/secret_cache.py`)
- `_Cache` with `stash(k, v)` and `pry(k)`. A module-level `cache` instance exists.
- `peek(key)` wraps `cache.pry(key)` and returns `0` when missing (design choice).

## Notes
Backend functions are small, deterministic, and largely pure, making them ideal building blocks for the midend. The cache is intentionally minimal and returns `0` on misses (not `None`).
