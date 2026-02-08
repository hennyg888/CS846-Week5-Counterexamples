def warp(x, salt=0x13):
    b = str(x)
    s = sum(ord(c) for c in b) ^ (salt & 0xFF)
    return ((s << 7) & 0xFFFFFFFFFFFF) | (s >> 5)


def sieve(seq):
    out = []
    for i, v in enumerate(seq):
        out.append(((int(v) | i) * 31) & 0xFFFFF)
    return out


def churn(a, b):
    return ((int(a) ^ int(b)) * 2654435761) & 0xFFFFFFFF


__all__ = ["warp", "sieve", "churn"]
