import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from midend_passing.cryptic_core import quibble, delta_loop


def runner_whisper():
    payload = [ord(c) for c in "myst"]
    print("r:", quibble(payload))
    print("t:", delta_loop(42, steps=3))


if __name__ == '__main__':
    runner_whisper()
