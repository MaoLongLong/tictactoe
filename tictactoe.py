# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2020/2/1
import numpy as np


class TicTacToeMove(object):
    def __init__(self, x_coordinate: int, y_coordinate: int, value: int):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value


class TicTacToeGameState(object):
    x = 1
    o = -1

    def __init__(self, state: np.ndarray, next_to_move: int = 1):
        self.board = state
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        row_sum = np.sum(self.board, 0)
        col_sum = np.sum(self.board, 1)
        tr = np.trace(self.board)
        tl = np.trace(self.board[::-1])

        if any(row_sum == 3) or any(col_sum == 3) or tr == 3 or tl == 3:
            return 1
        if any(row_sum == -3) or any(col_sum == -3) or tr == -3 or tl == -3:
            return -1
        if np.all(self.board != 0):
            return 0
        else:
            return None

    def is_game_over(self):
        return self.game_result is not None

    def is_move_legal(self, move: TicTacToeMove):
        if move.value != self.next_to_move:
            return False

        if move.x_coordinate < 0 or move.x_coordinate > 3:
            return False

        if move.y_coordinate < 0 or move.y_coordinate > 3:
            return False

        return self.board[move.x_coordinate, move.y_coordinate] == 0

    def move(self, move: TicTacToeMove):
        new_board = np.copy(self.board)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        next_to_move = self.x if self.next_to_move == self.o else self.o
        return TicTacToeGameState(new_board, next_to_move)

    def get_legal_actions(self):
        indices = np.where(self.board == 0)
        return [TicTacToeMove(coords[0], coords[1], self.next_to_move) for coords in
                list(zip(indices[0], indices[1]))]
