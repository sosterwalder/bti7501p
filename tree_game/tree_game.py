#!/usr/bin/env python
# tree_game.py - Provides a game interface for a given board (tree)
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Sven Osterwalder
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class TreeGame(object):
    """
    Provides a game interface for a given
    board (tree).

    Provides the following attributes:
        * current player
        * game state
        * terminal test
        * utility function
    """
    MAX_PLAYER = 'max'
    MIN_PLAYER = 'min'

    def __init__(self):
        """
        Constructor.
        """
        self.board = None
        self.terminal_states = [
            [
                [
                    [10, 11],
                    [9, 12]
                ],
                [
                    [14, 15],
                    [13, 14]
                ]
            ],
            [
                [
                    [5, 2],
                    [4, 1]
                ],
                [
                    [3, 22],
                    [20, 21]
                ]
            ]
        ]
        self.current_player = TreeGame.MAX_PLAYER
        self.moves = []
        self.depth = 0
        self.max_depth = 4

    def is_over(self):
        return self.evaluate_value() is not None

    def switch_player(self):
        if self.current_player == TreeGame.MAX_PLAYER:
            self.current_player = TreeGame.MIN_PLAYER

        else:
            self.current_player = TreeGame.MAX_PLAYER

    def make_move(self, move):
        self.moves.append(move)
        self.depth += 1

    def undo_move(self, move):
        self.moves.pop()
        self.depth -= 1

    def evaluate_value(self):
        val = self.terminal_states

        for move in self.moves:
            val = val[move]

        if type(val) is int:
            return val
        else:
            return None

    def successors(self):
        if self.current_player == TreeGame.MAX_PLAYER:
            if self.depth % 2 == 1 or self.depth == self.max_depth:
                return []

            else:
                return [0, 1]

        else:
            if self.depth % 2 == 0 or self.depth == self.max_depth:
                return []

            else:
                return [0, 1]
