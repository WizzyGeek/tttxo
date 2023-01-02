from itertools import chain
from typing import Literal
import numpy as np
from abc import ABC, abstractmethod as am


t = """┌─┬─┬─┐
│{}│{}│{}│
├─┼─┼─┤
│{}│{}│{}│
├─┼─┼─┤
│{}│{}│{}│
└─┴─┴─┘"""

class BoardFullError(Exception):
    """Board is Full"""

class Board:
    __slots__ = ("board", "open")
    r = np.arange(3)
    _s = list(chain(r, ((r, r), (r, r[::-1])), ((slice(None, None, None), 0), (slice(None, None, None), 1), (slice(None, None, None), 2))))
    _m = np.array([" ", "X", "O"])

    def __init__(self):
        self.board = np.zeros((3, 3), dtype=np.uint8)
        self.open = 9

    def play(self, p: int, m: Literal[1, 2]):
        if self.open == 0:
            raise BoardFullError("Board is Full")

        co = (p // 3, p % 3)
        if not self.board[co]:
            self.board[co] = m
            self.open -= 1
        else:
            raise ValueError("Cell already filled")

    def check_winner(self):
        b = self.board
        s = self._s
        for j in s:
            i = b[j]
            if i[0] and i[0] == i[1] == i[2]:
                return i[0]

    def __str__(self):
        return t.format(*(self._m[self.board.flatten()]))

class Interface(ABC):
    def __init__(self):
        pass

    @am
    def poll(self) -> int:
        return NotImplemented

    @am
    def write_updated_frame(self, board: Board):
        return NotImplemented

    @am
    def warn(self, msg: str):
        return NotImplemented

    @am
    def terminate(self):
        return NotImplemented

class BasicInterface(Interface):
    def __init__(self):
        pass

    def poll(self):
        while True:
            try:
                k = int(input("Enter Position: "))
            except (ValueError):
                self.warn("Need a number!")
                continue
            else:
                return k - 1

    def write_updated_frame(self, fboard: Board):
        print(t.format(*((string == " ") * str(idx)+ (string != " ") * string for idx, string in enumerate(Board._m[fboard.board.flatten()], 1))))

    def warn(self, msg: str):
        print(msg)

    def terminate(self):
        return super().terminate()

if __name__ == "__main__":
    # b = Board()
    # b.play(0, 1)
    # b.play(1, 2)
    # b.play(3, 1)
    # b.play(8, 1)
    # print(b)
    inter = BasicInterface()
    b = Board()
    m = 0
    while True:
        num = inter.poll()
        b.play(num, m + 1) # type: ignore
        m = (m + 1) % 2
        inter.write_updated_frame(b)
        winner = b.check_winner()
        if winner is not None:
            print(Board._m[winner], "won the game!")
            break
