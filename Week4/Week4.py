import time
from abc import ABC, abstractmethod


class Player:
    COLORS = ("white", "black")
    RESULTS = ("win", "loss", "draw", "not finished")

    def __init__(self, name, color):
        self._name = None
        self._color = None
        self._moves = 0
        self._captured = 0
        self._time_spent = 0.0
        self._result = "not finished"
        self.initialize(name, color)

    def initialize(self, name, color):
        self.set_name(name)
        self.set_color(color)

    def get_name(self):
        return self._name

    def get_color(self):
        return self._color

    def get_moves(self):
        return self._moves

    def get_captured(self):
        return self._captured

    def get_time_spent(self):
        return self._time_spent

    def get_result(self):
        return self._result

    def set_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Player name is required.")
        self._name = name.strip()

    def set_color(self, color):
        if color not in self.COLORS:
            raise ValueError(f"Color must be one of {self.COLORS}.")
        self._color = color

    def set_result(self, result):
        if result not in self.RESULTS:
            raise ValueError(f"Result must be one of {self.RESULTS}.")
        self._result = result

    def add_move(self, seconds, captured):
        self._moves += 1
        self._time_spent += seconds
        self._captured += captured

    def __repr__(self):
        return f"Player({self._name!r}, {self._color})"


class Checker:
    SYMBOLS = {("white", False): "w", ("white", True): "W", ("black", False): "b", ("black", True): "B"}

    def __init__(self, color, row, col):
        self._color = None
        self._row = None
        self._col = None
        self._king = False
        self.initialize(color, row, col)

    def initialize(self, color, row, col):
        if color not in Player.COLORS:
            raise ValueError(f"Color must be one of {Player.COLORS}.")
        self._color = color
        self.set_position(row, col)

    def get_color(self):
        return self._color

    def get_row(self):
        return self._row

    def get_col(self):
        return self._col

    def is_king(self):
        return self._king

    def set_position(self, row, col):
        if not isinstance(row, int) or not isinstance(col, int) or row < 0 or col < 0:
            raise ValueError("Position must be two non-negative whole numbers.")
        self._row = row
        self._col = col

    def directions(self):
        forward = -1 if self._color == "white" else 1
        rows = (forward, -forward) if self._king else (forward,)
        return [(dr, dc) for dr in rows for dc in (-1, 1)]

    def reaches_last_row(self, board_size):
        return (self._color == "white" and self._row == 0) or (self._color == "black" and self._row == board_size - 1)

    def promote(self):
        self._king = True

    def symbol(self):
        return self.SYMBOLS[(self._color, self._king)]

    def __repr__(self):
        kind = "King" if self._king else "Man"
        return f"Checker({self._color} {kind} at {self._row},{self._col})"


class Board(ABC):
    def __init__(self):
        self._grid = []
        self._checkers = []
        self.initialize()

    def initialize(self):
        self._grid = [[None] * self.size() for _ in range(self.size())]
        self._checkers = []
        for row in range(self.size()):
            for col in range(self.size()):
                if (row + col) % 2 == 1:
                    if row < self.piece_rows():
                        self._place(Checker("black", row, col))
                    elif row >= self.size() - self.piece_rows():
                        self._place(Checker("white", row, col))

    @abstractmethod
    def size(self):
        """Number of rows and columns."""
    @abstractmethod
    def piece_rows(self):
        """Rows of checkers each player starts with."""

    @abstractmethod
    def name(self):
        """Name of this board type."""

    def get_checker(self, row, col):
        return self._grid[row][col] if self.inside(row, col) else None

    def get_checkers(self, color=None):
        return [c for c in self._checkers if color is None or c.get_color() == color]

    def _place(self, checker):
        self._grid[checker.get_row()][checker.get_col()] = checker
        self._checkers.append(checker)

    def inside(self, row, col):
        return 0 <= row < self.size() and 0 <= col < self.size()

    def simple_moves(self, checker):
        """Squares one diagonal step away that are free."""
        result = []
        for dr, dc in checker.directions():
            row, col = checker.get_row() + dr, checker.get_col() + dc
            if self.inside(row, col) and self._grid[row][col] is None:
                result.append((row, col))
        return result

    def captures(self, checker):
        """Landing squares of jumps over an opponent piece onto a free square."""
        result = []
        for dr, dc in checker.directions():
            middle = self.get_checker(checker.get_row() + dr, checker.get_col() + dc)
            row, col = checker.get_row() + 2 * dr, checker.get_col() + 2 * dc
            if (middle is not None and middle.get_color() != checker.get_color()
                    and self.inside(row, col) and self._grid[row][col] is None):
                result.append((row, col))
        return result

    def legal_moves(self, color):
        """Every allowed (checker, target) pair. Capturing is mandatory, so jumps win over simple moves."""
        jumps = [(c, t) for c in self.get_checkers(color) for t in self.captures(c)]
        if jumps:
            return jumps
        return [(c, t) for c in self.get_checkers(color) for t in self.simple_moves(c)]

    def move(self, checker, row, col):
        """Move a checker. Returns (captured checker or None, True if it became a king)."""
        captured = None
        if abs(row - checker.get_row()) == 2:
            middle_row, middle_col = (row + checker.get_row()) // 2, (col + checker.get_col()) // 2
            captured = self._grid[middle_row][middle_col]
            self._grid[middle_row][middle_col] = None
            self._checkers.remove(captured)
        self._grid[checker.get_row()][checker.get_col()] = None
        checker.set_position(row, col)
        self._grid[row][col] = checker
        promoted = False
        if not checker.is_king() and checker.reaches_last_row(self.size()):
            checker.promote()
            promoted = True
        return captured, promoted

    def to_square(self, text):
        text = text.strip().lower()
        if len(text) < 2 or not text[0].isalpha() or not text[1:].isdigit():
            raise ValueError(f"'{text}' is not a square like c3.")
        col, row = ord(text[0]) - ord("a"), self.size() - int(text[1:])
        if not self.inside(row, col):
            raise ValueError(f"'{text}' is not on the board.")
        return row, col

    def to_text(self, row, col):
        return f"{chr(ord('a') + col)}{self.size() - row}"

    def status(self):
        white, black = self.get_checkers("white"), self.get_checkers("black")
        return (f"White: {len(white)} pieces ({sum(c.is_king() for c in white)} kings) | "
                f"Black: {len(black)} pieces ({sum(c.is_king() for c in black)} kings)")

    def show(self):
        letters = "   " + " ".join(chr(ord("a") + c) for c in range(self.size()))
        print(letters)
        for row in range(self.size()):
            cells = []
            for col in range(self.size()):
                checker = self._grid[row][col]
                cells.append(checker.symbol() if checker else ("." if (row + col) % 2 else " "))
            print(f"{self.size() - row:>2} " + " ".join(cells) + f" {self.size() - row}")
        print(letters)
        print(self.status())


class EnglishBoard(Board):
    def size(self):
        return 8

    def piece_rows(self):
        return 3

    def name(self):
        return "English checkers (8x8)"


class InternationalBoard(Board):
    def size(self):
        return 10

    def piece_rows(self):
        return 4

    def name(self):
        return "International draughts board (10x10)"


class Game:
    def __init__(self, player1, player2, board):
        """Constructor. player1 plays white and moves first."""
        self._players = []
        self._board = None
        self._current = 0
        self._moves = 0
        self._start = None
        self._end = None
        self._winner = None
        self.initialize(player1, player2, board)

    def initialize(self, player1, player2, board):
        """Initialization method."""
        if not isinstance(board, Board):
            raise TypeError("Expected a Board.")
        if {player1.get_color(), player2.get_color()} != {"white", "black"}:
            raise ValueError("One player must be white and the other black.")
        self._players = [player1, player2] if player1.get_color() == "white" else [player2, player1]
        self._board = board

    def get_players(self):
        return list(self._players)

    def get_board(self):
        return self._board

    def get_moves(self):
        return self._moves

    def get_duration(self):
        end = self._end if self._end is not None else time.time()
        return 0.0 if self._start is None else end - self._start

    def get_winner(self):
        return self._winner

    def current_player(self):
        return self._players[self._current]

    def other_player(self):
        return self._players[1 - self._current]

    def play(self, ask=input):
        """Run the game until a player wins or someone chooses to finish."""
        self._start = time.time()
        print(f"\n=== {self._board.name()} ===")
        while True:
            player = self.current_player()
            self._board.show()
            moves = self._board.legal_moves(player.get_color())
            if not moves:
                print(f"{player.get_name()} ({player.get_color()}) has no pieces or moves left.")
                self._finish(winner=self.other_player())
                break
            print(f"\nMove {self._moves + 1}: {player.get_name()} ({player.get_color()}), "
                  f"moves so far: {player.get_moves()}, time used: {player.get_time_spent():.0f} s")
            choice = ask("Type [m] to move or [f] to finish the game: ").strip().lower()
            if choice == "f":
                self._finish(winner=self._leader())
                break
            if choice != "m":
                print("Please type m or f.")
                continue
            turn_start = time.time()
            captured = self._take_turn(player, moves, ask)
            player.add_move(time.time() - turn_start, captured)
            self._moves += 1
            self._current = 1 - self._current
        self.summary()

    def _take_turn(self, player, moves, ask):
        """Ask for one move (and any follow-up jumps). Returns the number of captured pieces."""
        must_jump = abs(moves[0][1][0] - moves[0][0].get_row()) == 2
        if must_jump:
            print("You must capture. Possible jumps: " + ", ".join(
                f"{self._board.to_text(c.get_row(), c.get_col())}-{self._board.to_text(*t)}" for c, t in moves))
        while True:
            try:
                start_text, target_text = ask("Your move (e.g. c3 d4): ").split()
                start, target = self._board.to_square(start_text), self._board.to_square(target_text)
            except ValueError as error:
                print(f"Invalid input: {error}" if str(error) else "Please type two squares, e.g. c3 d4.")
                continue
            checker = self._board.get_checker(*start)
            if (checker, target) in moves:
                break
            print("That move is not allowed. Try again.")

        captured = 0
        while True:
            taken, promoted = self._board.move(checker, *target)
            print(f"{player.get_name()} moved {self._board.to_text(*start)} -> {self._board.to_text(*target)}"
                  + (" and captured a piece" if taken else "") + (" and became a king!" if promoted else ""))
            if taken is None:
                return captured
            captured += 1
            next_jumps = self._board.captures(checker)
            if promoted or not next_jumps:  
                return captured
            self._board.show()
            options = ", ".join(self._board.to_text(*t) for t in next_jumps)
            while True:
                try:
                    target = self._board.to_square(ask(f"Jump again with the same piece to ({options}): "))
                except ValueError as error:
                    print(f"Invalid input: {error}")
                    continue
                if target in next_jumps:
                    break
                print("That jump is not allowed.")
            start = (checker.get_row(), checker.get_col())

    def _leader(self):
        """When the game is finished early: the player with more pieces wins, equal pieces is a draw."""
        white = len(self._board.get_checkers("white"))
        black = len(self._board.get_checkers("black"))
        if white == black:
            return None
        return self._players[0] if white > black else self._players[1]

    def _finish(self, winner):
        self._end = time.time()
        self._winner = winner
        for player in self._players:
            if winner is None:
                player.set_result("draw")
            else:
                player.set_result("win" if player is winner else "loss")

    def summary(self):
        print("\n=========== Game summary ===========")
        print(f"Board: {self._board.name()}")
        print(f"Total moves: {self._moves}")
        print(f"Game time: {self.get_duration():.0f} s")
        print(f"Winner: {self._winner.get_name() if self._winner else 'draw'}")
        for p in self._players:
            print(f"- {p.get_name()} ({p.get_color()}): {p.get_result()}, moves {p.get_moves()}, "
                  f"captured {p.get_captured()}, time {p.get_time_spent():.0f} s")
        print(self._board.status())


def main():
    print("Welcome to Checkers!")
    white = Player(input("Name of player 1 (white, moves first): ") or "Player 1", "white")
    black = Player(input("Name of player 2 (black): ") or "Player 2", "black")
    kind = input("Board: [1] English 8x8 or [2] International 10x10? ").strip()
    board = InternationalBoard() if kind == "2" else EnglishBoard()
    Game(white, black, board).play()


if __name__ == "__main__":
    main()
