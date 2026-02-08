# Frontend Runners & Shims 🖥️

## Small examples & shims
- `main_entry.py` — constructs a seed, calls `snorfle` and `obscure_chain`, prints results.
- `runner.py` — builds a payload from a short string and prints outputs from `quibble` and `delta_loop`.
- `ghost_call.py` — demonstrates `wobble`, `fray`, and `loop_deque` outputs.
- `ui_shim.py` — `render_stub(payload)` maps `snorfle` → break into bytes → `quibble` and provides a `display(obj)` helper.
- `misnomer.py` — small utility that computes `snorfle(a) ^ wobble(a)`.

## Observations
- Frontends are deliberately thin and rely on the midend for heavy lifting.
- They add the package parent to `sys.path` for imports; this should be replaced with proper packaging or tests setting `PYTHONPATH`.
