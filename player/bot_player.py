#!/usr/bin/env python
# bot_player.py module
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
import random

# Project imports
# import controller.next_move             as next_move
import controller.player_interface      as player
import controller.board_element         as be
import algorithms.mini_max_alpha_beta   as mmab


class BotPlayer(player.PlayerInterface):
    def __init__(self):
        self.name = "BotPlayer"
        self.own_component = None
        self.oponent = None
        self.board_interface = None
        self.barrier = None
        self.weights = None

    def init(self, player, barrier, weights):
        self.own_component = player
        self.barrier = barrier
        self.weights = weights

        if self.own_component == be.BoardElement.player1:
            self.oponent = be.BoardElement.player2

        else:
            self.oponent = be.BoardElement.player1

        # print "{0}: Player is {1}".format(
        #     self.name, self.own_component
        # )

    def game_is_over(self, winner):
        return True

    def best_move(self, move, board_interface):
        # print "Trying to get best move"
        self.board_interface = board_interface

        if len(
            self.board_interface.all_moves_for_player(
                self.own_component
            )
        ) == 0:
            print "Got no moves for player {0} anymore".format(self.own_component)
            return None

        algorithm = mmab.MiniMaxAlphaBeta(
            self.weights,
            move,
            board_interface
        )
        value = algorithm.evaluate(
            -float('inf'),
            float('inf'),
            self.barrier,
            self.own_component
        )
        path = algorithm.path
        # print "Got paths {0} and value {1}".format(path, value)

        best_moves = []

        for element in path:
            if element[1] == value:
                best_moves.append(element[0])

            else:
                if len(best_moves) == 0 and len(path) != 0:
                    return path[0][0]

        # print "Got best moves {0}".format(best_moves)
        selected_move = random.choice(best_moves)

        return selected_move
