from backend_processing.arcane_tools import warp, sieve, churn
from backend_processing.core_back import sift_kit, flux
from backend_processing.secret_cache import cache


def wobble(z):
    c = warp(z, salt=(int(str(z)[-1]) if str(z) else 1))
    cache.stash(z, c)
    return c ^ 0xABC


def fray(seq):
    s = sieve(seq)
    return sum(s) ^ flux(len(seq))


def loop_deque(seed, n=4):
    r = seed
    for i in range(n):
        r = churn(r, sift_kit(str(r)))
    return [r & 0xFF for _ in range(n)]


__all__ = ["wobble", "fray", "loop_deque"]
