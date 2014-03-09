#!/usr/bin/env python
# negamax.py - An implementation of the NegaMax-algorithm
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


class Negamax(object):
    """
    Implementation of the NegaMax algorithm
    including alpha-beta-cutoff.

    Assumes that the first argument is a game
    class providing the following attributes:
        * current player
        * game state
        * terminal test
        * utility function
    """

    DEBUG = True
    INFINITY = float('inf')

    def evaluate(self, game, depth, alpha=+INFINITY, beta=-INFINITY):
        """
        Evaluates the best value and move
        for the given game.
        """

        if depth == 0 or game.is_over():
            game_value = game.evaluate_value()

            return game_value

        else:
            successors = game.successors()

            best_value = -Negamax.INFINITY

            for move in successors:
                game.make_move(move)
                game.switch_player()

                value = -self.evaluate(
                    game=game,
                    depth=depth - 1,
                    alpha=-beta,
                    beta=-alpha,
                )
                game.switch_player()
                game.undo_move(move)

                best_value = max(
                    best_value,
                    value
                )

                if alpha < value:
                    alpha = value

                    if alpha >= beta:
                        break

        return best_value
