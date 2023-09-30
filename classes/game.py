import numpy as np

class Game:
    def __init__(self, x, y):
        self._valid_data(x, y)
        self.x = x
        self.y = y
        self.board = self._create_board()

    def _valid_data(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError(f"Error, the values are not integer")

    def _create_board(self):
        return np.zeros((self.x, self.y), dtype=str)

    def place_piece(self, row, column):
        self.board[row, column] = 'x'

    def show_board(self):
        print(self.board)
