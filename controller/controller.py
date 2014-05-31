#!/usr/bin/env python
# board_interface.py module
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
import time

# Project imports
import board                as bboard
import board_element        as be
import player.bot_player    as bp
import action               as a
import util
import game_states          as gs


class Controller():
    ILLEGAL_MOVE_LIMIT = 50

    def __init__(
        self,
        number_of_rows,
        number_of_columns,
        weights,
        barrier,
        verbose=False
    ):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns

        self.weights = weights
        self.barrier = barrier

        self.do_output = verbose

        self.player1 = bp.BotPlayer()
        self.player1.init(
            be.BoardElement.player1,
            self.barrier,
            self.weights
        )
        self.player2 = bp.BotPlayer()
        self.player2.init(
            be.BoardElement.player2,
            self.barrier,
            self.weights
        )

        self.move = 0
        self.illegal_moves = 0
        self.board = bboard.Board()
        self.board.create(
            player1=self.player1,
            player2=self.player2,
            rows=self.number_of_rows,
            columns=self.number_of_columns,
            do_output=True
        )
        self.current_player = self.player1
        self.continue_playing = False
        self.game_is_over     = False
        self.winner = None

    def switch_player(self):
        if self.current_player.own_component == be.BoardElement.player1:
            self.current_player = self.player2

        else:
            self.current_player = self.player1

    def play(self):
        self.continue_playing = True

        while self.continue_playing:
            self.one_game()
            self.continue_playing = False

    def one_game(self):
        self.game_is_over = False  # False
        print "Starting game"
        print self.board

        while (not self.game_is_over) and self.illegal_moves < self.ILLEGAL_MOVE_LIMIT:
            if self.do_output:
                print "Current player is {0}, move {1}".format(
                    self.current_player.own_component,
                    self.move
                )
            best_move = self.current_player.best_move(self.move, self.board)
            if self.do_output:
                print "Got best move {0}".format(best_move)

            if best_move is None:
                self.winner = util.Util.switch_player(
                    self.current_player.own_component
                )
                break

            self.apply_action(best_move)

            if self.do_output:
                print self.board
                print "Score: {0}".format(self.board.score(self.weights))
                print "No. of illegal moves {0}".format(self.illegal_moves)
                time.sleep(1)

        if self.illegal_moves >= self.ILLEGAL_MOVE_LIMIT:
            print "Reached limit of >= {0} illegal moves!".format(
                self.ILLEGAL_MOVE_LIMIT
            )

        if not self.game_is_over:
            self.winner = gs.GameStates.STATE_DRAW

        print "Game has finished"
        print self.board
        return self.winner

    def apply_action(self, action):
        self.board.apply_action(action)
        self.move += 1

        if len(self.board.first_player_pieces) == 0:
            self.game_is_over = True
            self.winner = be.BoardElement.player2

        elif len(self.board.second_player_pieces) == 0:
            self.game_is_over = True
            self.winner = be.BoardElement.player1

        else:
            self.switch_player()

            if action.type_ != a.Action.ACTION_UNDO:
                self.illegal_moves += 1

            else:
                self.illegal_moves = 0
