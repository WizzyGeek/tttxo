from tttxo.utils import BoardFullError, Interface, Board

class Game:
    def __init__(self, board: Board, interface: Interface) -> None:
        self.b = board
        self.inter = interface
        self.player = 0

    def write_turn(self, prompt: bool = True):
        if self.b.open and prompt:
            self.inter.warn(f"{self.b._m[(self.player % 2) + 1]}'s Turn!")
        self.inter.write_updated_frame(self.b)

    def play_move(self, p: int) -> bool:
        if self.b.open == 0:
            self.inter.warn("Tie!")
            return True

        try:
            self.b.play(p, (self.player % 2) + 1) # type: ignore
        except ValueError:
            self.inter.warn("That postion is already filled!\n")
            return False
        except BoardFullError:
            self.inter.warn("Tie!")
            return True
        else:
            self.player += 1

        winner = self.b.check_winner()
        if winner is not None:
            self.inter.warn(str(Board._m[winner]) + " won the game!\n")
            return True
        if self.b.open == 0:
            self.inter.warn("Tie!\n")
            return True
        return False

    def rpul(self): # Repeated poll and update loop
        self.write_turn()
        # self.inter.write_updated_frame(self.b)
        # self.write_turn()
        while True:
            try:
                m = self.inter.poll()
            except KeyboardInterrupt:
                self.inter.terminate()
                break
            br = self.play_move(m)
            self.write_turn(not br)
            if br:
                self.inter.warn("[Continue to Exit]")
                self.inter.poll()
                self.inter.terminate()
                break

if __name__ == "__main__":
    from tttxo.curses_inter import BasicCursesInterface
    g = Game(Board(), BasicCursesInterface())
    g.rpul()