from dataclasses import dataclass
from string import ascii_lowercase


@dataclass
class Coord:

    @staticmethod
    def build_from_str(s):
        return Coord(ascii_lowercase.index(s[0]), int(s[1]))

    @staticmethod
    def get_row_from_num(num, width=8):
        return ascii_lowercase[:width][num]

    row: int
    col: int

    def __str__(self):
        return Coord.get_row_from_num(self.row, 8) + str(self.col)

    def check(self, width=8, height=8):
        if Coord.get_row_from_num(self.row, 8) not in ascii_lowercase[:width] or \
                self.col < 1 or \
                self.col > height:
            return False

        return True

    def __getitem__(self, item):
        if item == 0:
            return self.row
        elif item == 1:
            return self.col
        else:
            raise IndexError('Invalid format')
