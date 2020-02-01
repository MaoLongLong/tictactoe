# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2020/2/1
from collections import defaultdict

import numpy as np

from tictactoe import TicTacToeGameState


class MonteCarloTreeSearchNode(object):
    def __init__(self, state: TicTacToeGameState, parent=None):
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self.state = state
        self.parent = parent
        self.children = []
        self.untried_actions = self.state.get_legal_actions()

    @property
    def q(self):
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def roll_out(self):
        current_roll_out_state = self.state
        while not current_roll_out_state.is_game_over():
            possible_moves = current_roll_out_state.get_legal_actions()
            action = self.roll_out_policy(possible_moves)
            current_roll_out_state = current_roll_out_state.move(action)
        return current_roll_out_state.game_result

    def back(self, result):
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.back(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt(2 * np.log(self.n) / c.n)
            for c in self.children
        ]
        return self.children[int(np.argmax(choices_weights))]

    @staticmethod
    def roll_out_policy(possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]
