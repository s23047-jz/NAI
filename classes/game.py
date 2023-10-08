import numpy as np
from easyAI import TwoPlayerGame


class Game(TwoPlayerGame):
    def __init__(self, players):
        self.rows = 6
        self.cols = 7
        self.players = players
        self.move_counter = 0
        self.board = self._create_board()
        self.current_player = 1

    def _create_board(self):
        """
        Creates game board
        """
        return np.zeros((self.rows, self.cols), dtype=str)

    def pos_dir(self):
        """

        :return:
            Returns an array of positions with a possibly found streak
        """
        # TODO try find another way
        return np.array(
        [[[i, 0], [0, 1]] for i in range(6)]
        + [[[0, i], [1, 0]] for i in range(7)]
        + [[[i, 0], [1, 1]] for i in range(1, 3)]
        + [[[0, i], [1, 1]] for i in range(4)]
        + [[[i, 6], [1, -1]] for i in range(1, 3)]
        + [[[0, i], [1, -1]] for i in range(3, 7)]
        )

    def _find_four(self):
        """
        :return:
            Returns whether any player has a streak or not
        """
        for pos, direction in self.pos_dir():
            streak = 0
            while (0 <= pos[0] < self.rows) and (0 <= pos[1] < self.cols):
                if self.board[pos[0], pos[1]] == self._get_current_player_character(self.opponent_index):
                    streak += 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
                pos = pos + direction
        return False

    def _get_current_player_character(self, player_index):
        """
        :param:
            player_index: int - players id
        :return:
        Returns players character
        """
        return 'O' if player_index == 2 else 'X'

    def possible_moves(self):
        """
        :return:
        Returns an array of possible moves
        """
        return [c for c in range(self.cols) if self.board[0][c] == '']

    def make_move(self, column):
        """
        :param:
            column: int - Selected column to input character
        """
        row = max([r for r in range(self.rows) if self.board[r][column] == ''])
        self.board[row][column] = self._get_current_player_character(self.current_player)

    def lose(self):
        return self._find_four()

    def is_over(self):
        return len(self.possible_moves()) == 0 or self.lose()

    def scoring(self):
        return -100 if self.lose() else 0

    def show(self):
        print(self.board)
