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

    INFINITY = float('inf')

    def __init__(self, game):
        """
        Constructor.
        """
        self.game       = game
        self.best_value = -Negamax.INFINITY
        self.best_move  = None
        self.proposal   = {
            'value':    self.best_value,
            'move':     self.best_move,
        }

    def evaluate(self, game, depth):
        """
        Evaluates the best value and move
        for the given game.
        """

        if depth == 0 or self.game.is_over():
            return self.game.evaluate_value()

        for move in game.moves:
            game.make_move(move)
            value = -self.evaluate()
            game.undo_move(move)

            if value > self.best_value:
                self.best_value = value
                self.best_move = move

        return self.proposal
