# Midend Composition & Engines ⚙️

## `cryptic_core.py` (composed primitives)
- `snorfle(key, twist=7)` — XOR/text transform, SHA-256, map to integer, then calls `tangle` for final mixing.
- `quibble(items)` — aggregate multiply-and-xor using `flux` to produce a wide accumulator.
- `delta_loop(seed, steps=5)` — PRNG-like sequence derived from LCG-style update plus `tangle` mixing.
- `_HiddenEngine.hum(base).` Internal helper: uses `sift_kit` and base digits to compute a scalar.
- `obscure_chain(x, y=None)` — builds `engine`, gets `token = snorfle(y or x)`, computes chain via `sift_kit` and mixes with `tangle`.

## `muddle.py` (front-facing transforms that use backend primitives)
- `wobble(z)` — computes `warp(z, salt=...)`, stores result with `cache.stash(z, c)`, returns `c ^ 0xABC`.
- `fray(seq)` — applies `sieve(seq)`, sums results, then xors with `flux(len(seq))`.
- `loop_deque(seed, n)` — iterative loop: `r = churn(r, sift_kit(str(r)))`; returns list of bytes.

## Design notes
Midend functions are glue: they use backend primitives to produce predictable tokens and sequences. They also mutate the `cache` via `wobble`, coupling a side-effect to an otherwise pure transform.
