import numpy as np
from typing import Any


class Game:
    def __init__(self, x: int, y: int):
        self._valid_data(x, y)
        self.x = x
        self.y = y
        self.board = self._create_board()
        self.move_counter = 0

    def _valid_data(self, x: Any, y: Any):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Error, the values are not integer")

    def _create_board(self):
        return np.zeros((self.x, self.y), dtype=str)

    def _valid_move(self, row):
        return self.board[row, 0] == ''

    def place_piece(self, row: int, column: int):
        self.board[row, column] = 'x'

    def show_board(self):
        print(self.board)
