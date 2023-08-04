import string

from src.coord import Coord
from typing import Any


class Board:

    WIDTH = 8
    HEIGHT = 8

    board: list[list[Any | None]]

    def __init__(self):
        self.board = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

        self.row_name = {i: x for x, i in enumerate(string.ascii_lowercase) if x + 1 <= self.WIDTH}
        self.col_name = {str(i): i - 1 for i in range(1, self.HEIGHT + 1)}

    def __getitem__(self, item: str | tuple[str, str] | Coord):
        if len(item) != 2:
            raise IndexError('Invalid format')

        row, col = item[0], item[1]

        if row not in self.row_name or col not in self.col_name:
            raise IndexError('Invalid format')

        return self.board[self.row_name[row]][self.col_name[col]]

    def __setitem__(self, key, value):
        if len(key) != 2:
            raise IndexError('Invalid format')

        row, col = key[0], key[1]

        if row not in self.row_name or col not in self.col_name:
            raise IndexError('Invalid format')

        self.board[self.row_name[row]][self.col_name[col]] = value

    def get_height(self, n):
        return self.board[n]

    def get_width(self, n):
        return list(map(lambda x: x[n], self.board))

    def is_occupied(self, coord):
        return self[coord] is not None

    def is_check(self, color):
        pass

    def is_checkmate(self, color):
        pass

    def can_move(self, color):
        return not (self.is_check(color) or self.is_checkmate(color))

    def actual_color(self):
        pass





