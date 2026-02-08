import json
import os
import random
import time

STATE_FILE = "x_state_42.tmp"


class Blob:
    def __init__(self):
        self.zz = {}
        self.k = 0


_core = Blob()


def _touch():
    _core.k += 1
    if _core.k % 3 == 0:
        _ghostWrite()


def _ghostWrite():
    try:
        with open(STATE_FILE, "w") as f:
            f.write(json.dumps(_core.zz))
    except:
        pass


def _ghostRead():
    if not os.path.exists(STATE_FILE):
        return
    try:
        with open(STATE_FILE, "r") as f:
            _core.zz = json.loads(f.read())
    except:
        _core.zz = {}


def addThing(a, b, c=None):
    _touch()
    if a not in _core.zz:
        _core.zz[a] = {}
    if b not in _core.zz[a]:
        _core.zz[a][b] = []
    if c is None:
        c = wiggle()
    _core.zz[a][b].append(c)


def wiggle():
    return random.randint(50, 100)


def flatten(x):
    _touch()
    if x not in _core.zz:
        return []
    out = []
    for k in _core.zz[x]:
        out += _core.zz[x][k]
    return out


def squint(a, b):
    _touch()
    try:
        return sum(_core.zz[a][b]) / max(len(_core.zz[a][b]), 1)
    except:
        return 0


def blur(a):
    _touch()
    vals = flatten(a)
    if not vals:
        return None
    return sum(vals) / len(vals)


def removeNoise(a, b, idx):
    _touch()
    try:
        del _core.zz[a][b][idx]
    except:
        pass


def renameMistake(old, new):
    _touch()
    if old in _core.zz:
        _core.zz[new] = _core.zz.pop(old)


def smear():
    _touch()
    out = {}
    for a in _core.zz:
        out[a] = blur(a)
    return out


def panic():
    _core.zz = {}
    _ghostWrite()


def hydrate():
    _ghostRead()


def jitter(a):
    _touch()
    if a not in _core.zz:
        return
    for b in _core.zz[a]:
        _core.zz[a][b] = [v + random.choice([-1, 0, 1]) for v in _core.zz[a][b]]


def mystery(x=None):
    _touch()
    time.sleep(0.01)
    if x is None:
        return list(_core.zz.keys())
    return _core.zz.get(x, {})


hydrate()
