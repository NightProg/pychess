from coord import Coord


class Piece:
    def __init__(self, name, movement):
        self.killed = False
        self.name = name
        self.movement = movement

    def check(self, board, coord):
        for mov in self.movement:
            if mov[0].check(board, coord):
                return True
        return False

    def move(self, board, coord):
        if self.check(board, coord):
            for mov in self.movement:
                if (coord.col, coord.row) in mov[1].get_moves():
                    board[coord] = self.name


class Rule:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def check(self, board, coord):
        return True


class IsCorrectCoord(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def check(self, board, coord):
        return board.WIDTH > coord.row > 0 and board.HEIGHT > coord.col > 0


class CanPlay(Rule):
    def check(self, board, coord):
        color = board.actual_color()
        return not (board.is_check(color) or board.is_checkmate(color))


class When(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.coords = list(map(Coord.build_from_str, self.args))

    def check(self, board, coord):
        return coord in self.coords


class Or(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rules = self.args

    def check(self, board, coord):
        for rule in self.rules:
            if rule.check(board, coord):
                return True

        return False


class And(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rules = self.args

    def check(self, board, coord):
        for rule in self.rules:
            if not rule.check(board, coord):
                return False

        return True


class Void(And):
    def __init__(self):
        self.rules = [IsCorrectCoord(), CanPlay()]


class WhenOccupied(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check(self, board, coord):
        return board.is_occupied(coord)


class WhenEmpty(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check(self, board, coord):
        return not board.is_occupied(coord)


class Movement:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def get_moves(self, board, coord):
        return []


class MovCoord(Movement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = self.args[0]
        self.col = self.args[1]

    def get_moves(self, board, _coord):
        return [[self.row, self.col]]


class MovSuiteOfCoord(Movement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = self.args[0]
        self.y = self.args[1]

    def get_moves(self, board, coord):
        start_1 = [[0, 0]]
        start_2 = [[0, 0]]
        limit = abs(coord.col - 8)

        for i in range(limit):
            if start_1[-1][0] + self.x > 8 or start_1[-1][1] + self.y > 8:
                continue
            start_1.append([start_1[-1][0] + self.x, start_1[-1][1] + self.y])

        for i in range(board.HEIGHT - limit):
            if start_2[-1][0] - self.x < -8 or start_2[-1][1] - self.y < -8:
                continue
            start_2.append([start_2[-1][0] - self.x, start_2[-1][1] - self.y])
        start_1.extend(start_2)
        start_1.remove([0, 0])
        start_1.remove([0, 0])
        return start_1


pawn_rule_jump_2 = And(
    When("a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"),
    WhenEmpty()
)


pawn = Piece("Pawn", [
    [pawn_rule_jump_2, MovCoord(0, 2)],
    [Void(), MovCoord(0, 1)],
    [And(WhenOccupied(), Void()), MovCoord(1, 1)],
    [And(WhenOccupied(), Void()), MovCoord(-1, 1)],
])

knights = Piece("Knight", [
    [Void(), MovCoord(2, 1)],
    [Void(), MovCoord(1, 2)],
    [Void(), MovCoord(-2, 1)],
    [Void(), MovCoord(-1, 2)],
    [Void(), MovCoord(2, -1)],
    [Void(), MovCoord(1, -2)]
])

Bishop = Piece("Bishop", [
    [Void(), MovSuiteOfCoord(1, 1)],
])

Rook = Piece("Rook", [
    [Void(), MovSuiteOfCoord(1, 0)],
    [Void(), MovSuiteOfCoord(0, 1)],
])

Queen = Piece("Queen", [
    [Void(), MovSuiteOfCoord(1, 1)],
    [Void(), MovSuiteOfCoord(1, 0)],
    [Void(), MovSuiteOfCoord(0, 1)],
])


