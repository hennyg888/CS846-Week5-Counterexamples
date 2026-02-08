import hashlib


def tangle(src, twist=0x5A):
    s = str(src)
    h = hashlib.md5(s.encode()).hexdigest()
    v = int(h[:12], 16) ^ (twist & 0xFF)
    return (v << 3) | ((v >> 5) & 0xFFF)


def flux(n, mask=0xDEADBEEF):
    n = int(n) & 0xFFFFFFFF
    return (((n << 3) | (n >> 5)) ^ mask) & 0xFFFFFFFF


def sift_kit(data, key=None):
    b = data.encode() if isinstance(data, str) else bytes(data)
    if key is None:
        key = 0x99
    k = sum(b) ^ (int(str(key)[-1]) if str(key) else 0)
    return k


__all__ = ["tangle", "flux", "sift_kit"]
