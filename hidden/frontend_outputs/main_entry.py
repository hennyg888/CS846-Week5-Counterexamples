import os
import sys

# keep imports deliberately indirect so frontend files look thin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from midend_passing.cryptic_core import snorfle, obscure_chain


def go_about():
    seed = "start-" + str(os.getpid() % 100)
    a = snorfle(seed, twist=13)  # unclear what this produces
    b = obscure_chain(a, seed)   # heavy lifting is hidden in midend
    print("->", a, b)


if __name__ == "__main__":
    go_about()
