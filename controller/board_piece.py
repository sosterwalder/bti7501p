#!/usr/bin/env python
# board_piece.py module
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
import action        as action
import board_element as be


class BoardPiece(object):
    def __init__(self, board_interface, row, column, board_element):
        self.board_interface = board_interface
        self.position = (row, column)
        self.board_element = board_element

    def get_features(self):
        features_list = []
        board_element = self.board_element
        row, column = self.position

        features_list = [be.BoardElement.piece]

        if row < 3:
            if board_element == be.BoardElement.player1:
                features_list = [be.BoardElement.piece, be.BoardElement.front]

            else:
                features_list = [be.BoardElement.piece, be.BoardElement.back]

        if row >= 4:
            if board_element == be.BoardElement.player1:
                features_list = [be.BoardElement.piece, be.BoardElement.back]

            else:
                features_list = [be.BoardElement.piece, be.BoardElement.front]

        if row == 3:
            features_list.append(be.BoardElement.center)

        return features_list

    def move(self, new_row, new_column):
        new_position = (new_row, new_column)
        self.board_interface.set_bitmap(
            self.position[0],
            self.position[1],
            None
        )
        self.board_interface.set_bitmap(
            new_row,
            new_column,
            self
        )
        self.position = new_position

    def captured(self):
        self.board_interface.set_bitmap(
            self.position[0],
            self.position[1],
            None
        )

    def _possible_action_piece(self):
        is_free = self.board_interface.is_free
        board = self.board_interface

        moves = []
        row, col = self.position
        can_capture = False

        for delta_row in (-1, 0, 1):
            for delta_column in (-1, 0, 1):
                if delta_row == 0 and delta_column == 0:
                    continue

                current_move = (
                    row + delta_row,
                    col + delta_column
                )
                #print "Piece {0} for player {1}: Trying {2}".format(self.position, self.board_element, current_move)
                obstruction_move = (
                    row + 2 * delta_row,
                    col + 2 * delta_column
                )

                if is_free(
                    current_move[0],
                    current_move[1]
                ):
                    #print "Piece {0} for player {1}: Is free".format(self.position, self.board_element)
                    if not can_capture:
                        moves.append(
                            action.Action(
                                'MOVE',
                                (row, col),
                                current_move
                            )
                        )

                elif is_free(
                    obstruction_move[0],
                    obstruction_move[1]
                ):
                    obstructed_piece = board.get_piece(
                        current_move[0],
                        current_move[1]
                    )

                    if obstructed_piece.board_element != self.board_element:
                        moves.append(
                            action.Action(
                                'CAPTURE',
                                (row, col),
                                obstruction_move,
                                obstructed_piece
                            )
                        )
                        can_capture = True

        if can_capture:
            new_moves = []

            for move in moves:
                if move.type_ == 'CAPTURE':
                    new_moves.append(move)

            return new_moves

        return moves

    def possible_action(self):
        return self._possible_action_piece()
