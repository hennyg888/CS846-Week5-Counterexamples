import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from midend_passing.cryptic_core import snorfle, quibble


def render_stub(payload):
    # deliberately terse: transform input via midend, then map to an aggregate
    t = snorfle(payload)
    return quibble([t & 0xFF, (t >> 8) & 0xFF, (t >> 16) & 0xFF])


# small shim function exposed by frontend
def display(obj):
    print("out:", render_stub(obj))
