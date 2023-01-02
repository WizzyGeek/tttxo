import imp
from tttxo.game import Game
try:
    from tttxo.curses_inter import BasicCursesInterface as Inter
except (ImportError, ModuleNotFoundError):
    from tttxo.utils import BasicInterface as Inter

from tttxo.utils import Board

def main():
    while True:
        g = Game(Board(), Inter())
        g.rpul()
        try:
            a = input("Play Again? [Y/n]: ").lower()
        except KeyboardInterrupt:
            return
        if not a or a[0] == "y":
            ret = False
        else:
            ret = True
        if ret:
            break
    return