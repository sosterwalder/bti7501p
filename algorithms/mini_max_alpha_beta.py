#!/usr/bin/env python
# mini_max_alpha_beta.py module
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

# System imports

# Project imports
import controller.board_element     as be
import controller.util              as util


class MiniMaxAlphaBeta(object):
    def __init__(
        self,
        weights,
        move,
        board_interface
    ):
        self.weights = weights
        self.move = move
        self.board_interface = board_interface
        self.path = []

    def evaluate(self, alpha, beta, level, player):
        if level == 0:
            value = self.board_interface.score(self.weights)
            # print "Appending path"
            self.path.append((
                self.board_interface.move_history[self.move],
                value
            ))
            # print "Path {0}".format(self.path)

            return value

        if player == be.BoardElement.player1:
            moves = self.board_interface.all_moves_for_player(player)
            value = -float('inf')

            for move in moves:
                self.board_interface.apply_action(move)
                value = max(value, self.evaluate(
                    alpha, beta, level - 1, util.Util.switch_player(player)
                ))
                self.board_interface.undo_last_action()

                if beta <= value:
                    return value

                alpha = max(alpha, value)

            if len(moves) == 0:
                self.path.append((
                    self.board_interface.move_history[self.move],
                    value
                ))
                # print "Path {0}".format(self.path)

            return value

        else:
            moves = self.board_interface.all_moves_for_player(player)
            value = float('inf')

            for move in moves:
                self.board_interface.apply_action(move)
                value = min(
                    value,
                    self.evaluate(
                        alpha,
                        beta,
                        level - 1,
                        util.Util.switch_player(player)
                    )
                )
                self.board_interface.undo_last_action()

                if value <= alpha:
                    return value

                beta = min(beta, value)

            if len(moves) == 0:
                self.path.append((
                    self.board_interface.move_history[self.move],
                    value
                ))
                # print "Path {0}".format(self.path)

            return value
