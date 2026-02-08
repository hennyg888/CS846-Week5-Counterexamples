import hashlib
from backend_processing.core_back import tangle, flux, sift_kit


def snorfle(key, twist=7):
    s = ''.join(chr((ord(c) ^ twist) & 0xFF) for c in str(key))
    h = hashlib.sha256(s.encode()).hexdigest()
    v = int(h[:16], 16) ^ twist
    return tangle(v, twist=twist)


def quibble(items):
    acc = 1
    for i in items:
        acc = (acc * (flux(int(i)) ^ 0xDEADBEEF)) & 0xFFFFFFFFFFFF
    return acc


def delta_loop(seed, steps=5):
    r = int(seed) & 0xFFFFFFFF
    seq = []
    for i in range(steps):
        r = (r * 1664525 + 1013904223) ^ (i << 3) ^ (tangle(r) & 0xFFFF)
        seq.append(r & 0xFFFFFFFF)
    return seq


class _HiddenEngine:
    def __init__(self, base):
        self.base = base

    def hum(self, n):
        k = sift_kit(str(self.base), n)
        return sum(int(x) for x in str(self.base)) * (k & 0xFF)


def obscure_chain(x, y=None):
    engine = _HiddenEngine(x)
    token = snorfle(y or x)
    chain = sift_kit(str(token), x)
    return (engine.hum(token) ^ tangle(chain)) & 0xFFFFFFFF


__all__ = ["snorfle", "quibble", "delta_loop", "obscure_chain"]
