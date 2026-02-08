import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from midend_passing.muddle import wobble, fray, loop_deque


def do_ghost(x):
    print("G:", wobble(x))
    print("F:", fray([ord(c) for c in str(x)]))
    print("L:", loop_deque(12345))


if __name__ == '__main__':
    do_ghost("z")
