# -*- coding: utf-8 -*-
# author: MaoLongLong
# date: 2020/2/1
import sys
import tkinter as tk
from tkinter import messagebox

import numpy as np

from mcts.nodes import MonteCarloTreeSearchNode
from mcts.search import MonteCarloTreeSearch
from tictactoe import TicTacToeGameState


class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.first = None
        self.state = TicTacToeGameState(np.zeros((3, 3)))
        self.cv = tk.Canvas(self)
        self.start_btn = tk.Button(self, text='开始游戏', command=self.start)
        self.setup_ui()

    def setup_ui(self):
        self.title('TicTacToe')
        self.geometry('480x480')
        self.start_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        for i in range(160, 321, 160):
            self.cv.create_line(20, i, 460, i, width=5, fill='orange')
            self.cv.create_line(i, 20, i, 460, width=5, fill='orange')
        self.cv.pack(fill=tk.BOTH, expand=tk.YES)
        self.cv.bind('<Button-1>', self.on_click)

    def computer(self):
        node = MonteCarloTreeSearchNode(self.state)
        tree = MonteCarloTreeSearch(node)
        best_node = tree.best_action(1000)
        temp = best_node.state.board
        for i in range(3):
            for j in range(3):
                if temp[i, j] != self.state.board[i, j]:
                    self.draw_chess(i, j, self.state.next_to_move)
                    break
        self.state = best_node.state

    def judge(self):
        if self.state.is_game_over():
            res = self.state.game_result
            if res == 1 and self.first or res == -1 and not self.first:
                mes = '你赢了'
            elif res == 1 and not self.first or res == -1 and self.first:
                mes = '你输了'
            else:
                mes = '平局'
            tk.messagebox.showinfo('TicTacToe', mes)
            self.quit()
            sys.exit(0)

    def start(self):
        ok = tk.messagebox.askyesno('TicTacToe', '是否先手？')
        if not ok:
            self.first = False
            self.computer()
        else:
            self.first = True
        self.start_btn.destroy()

    def on_click(self, event):
        i = (event.y - 20) // 160
        j = (event.x - 20) // 160
        if self.first is not None and self.state.board[i, j] == 0:
            self.state.board[i, j] = self.state.next_to_move
            self.draw_chess(i, j, self.state.next_to_move)
            self.state.next_to_move = TicTacToeGameState.x \
                if self.state.next_to_move == TicTacToeGameState.o else TicTacToeGameState.o

            self.judge()

            self.computer()
            self.judge()

    def draw_chess(self, i, j, t):
        if t == TicTacToeGameState.x:
            self.cv.create_line(160 * j + 30,
                                160 * i + 30,
                                160 * j + 130,
                                160 * i + 130,
                                width=5,
                                fill='skyblue')
            self.cv.create_line(160 * j + 130,
                                160 * i + 30,
                                160 * j + 30,
                                160 * i + 130,
                                width=5,
                                fill='skyblue')
        else:
            self.cv.create_oval(160 * j + 30,
                                160 * i + 30,
                                160 * j + 130,
                                160 * i + 130,
                                width=5,
                                outline='chartreuse')


if __name__ == '__main__':
    game = Game()
    game.mainloop()
