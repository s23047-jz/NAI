import numpy as np
from easyAI import TwoPlayerGame, Negamax
from easyAI.games import ConnectFour


class Game(TwoPlayerGame):
    def __init__(self, players):
        self.rows = 7
        self.cols = 6
        self.players = players
        self.move_counter = 0
        self.board = self._create_board()

    def _create_board(self):
        return np.zeros((self.rows, self.cols), dtype=str)

    def _find_four(self):
        for row, col in self.board:
            streak = 0
            while (0 <= row[0] <= 5) and (0 <= row[1] <= 6):
                # TODO implement current player char
                if self.board[row[0], row[1]] == self._get_current_player_character(2):
                    streak += 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
                row = row + col
        return False

    def _get_current_player_character(self, player_index):
        return 'O' if player_index == 2 else 'X'

    def possible_moves(self):
        return [c for c in range(self.rows) if self.board[0][c] == '']

    def make_move(self, column):
        row = max([r for r in range(self.cols) if self.board[r][column] == ''])
        # TODO implement current player char
        self.board[row][column] = self._get_current_player_character(2)

    def lose(self):
        return self._find_four()

    def is_over(self):
        return len(self.possible_moves()) == 0 or self.lose()

    def show(self):
        print(self.board)
