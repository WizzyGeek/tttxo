from tttxo.utils import Interface, Board
import curses

class BasicCursesInterface(Interface):
    def __init__(self) -> None:
        self.stdscr = scr = curses.initscr()
        self.pos = [0, 0]
        scr.keypad(True)
        curses.noecho()
        curses.cbreak()
        self.board_win = curses.newwin(8, 8, 0, 0)
        self.warn_win = curses.newwin(curses.LINES - 8, curses.COLS, 8, 0)
        self.help_win = curses.newwin(8, curses.COLS - 8, 0, 8)
        scr.refresh()
        self.help_win.addstr("\nArrow keys to move\nctrl + c to exit")
        self.help_win.refresh()

    def terminate(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def poll(self):
        self.warn_win.clear()
        while True:
            key = self.stdscr.getkey()
            if key == "KEY_UP":
                self.pos[0] = (self.pos[0] - 1) % 3
            elif key == "KEY_DOWN":
                self.pos[0] = (self.pos[0] + 1) % 3
            elif key == "KEY_LEFT":
                self.pos[1] = (self.pos[1] - 1) % 3
            elif key == "KEY_RIGHT":
                self.pos[1] = (self.pos[1] + 1) % 3
            elif key == "\n":
                return self.pos[0] * 3 + self.pos[1]
            self.stdscr.move(self.pos[0] * 2 + 1, self.pos[1] * 2 + 1)
            curses.doupdate()

    def warn(self, msg: str):
        self.stdscr.refresh()
        self.warn_win.addstr(msg)
        self.warn_win.refresh()

    def write_updated_frame(self, b: Board):
        self.stdscr.refresh()
        self.board_win.clear()
        self.board_win.addstr(str(b))
        self.board_win.refresh()
        self.stdscr.move(self.pos[0] * 2 + 1, self.pos[1] * 2 + 1)
        curses.doupdate()

if __name__ == "__main__":
    # b = Board()
    # b.play(0, 1)
    # b.play(1, 2)
    # b.play(3, 1)
    # b.play(8, 1)
    # print(b)
    inter = BasicCursesInterface()
    b = Board()
    m = 0
    inter.write_updated_frame(b)
    while True:
        inter.write_updated_frame(b)
        num = inter.poll()
        try:
            b.play(num, m + 1) # type: ignore
        except ValueError:
            inter.warn("Positon already filled!\n")
            continue
        inter.write_updated_frame(b)
        m = (m + 1) % 2
        winner = b.check_winner()
        # inter.warn(str(winner)+"\n")
        if winner is not None:
            inter.warn(str(Board._m[winner]) + " won the game!\n")
            break
        if b.open == 0:
            inter.warn("Tie!\n")
            break
    inter.poll()
    inter.stdscr.clear()
    inter.terminate()

