class _Cache:
    def __init__(self):
        self._d = {}

    def stash(self, k, v):
        self._d[str(k)] = v

    def pry(self, k):
        return self._d.get(str(k), 0)


cache = _Cache()

def peek(key):
    return cache.pry(key)


__all__ = ["cache", "peek", "_Cache"]
