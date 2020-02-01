# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2020/2/1
from mcts.nodes import MonteCarloTreeSearchNode


class MonteCarloTreeSearch(object):
    def __init__(self, node: MonteCarloTreeSearchNode):
        self.root = node

    def best_action(self, simulations_number):
        for _ in range(simulations_number):
            v = self.tree_policy()
            reward = v.roll_out()
            v.back(reward)
        return self.root.best_child(c_param=0)

    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
