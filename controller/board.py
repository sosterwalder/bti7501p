#!/usr/bin/env python
# board.py module
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
import numpy                as np

# Project imports
import action               as a
import board_interface      as bi
import board_element        as be
import board_piece          as bp


class Board(object):
    MIN_ROWS  = 5
    MIN_COLUMNS = 5

    def __init__(self):
        self.rows = Board.MIN_ROWS
        self.columns = Board.MIN_COLUMNS

        self.first_player_pieces = []
        self.is_first_player_cached = False
        self.first_player_cache = None

        self.second_player_pieces = []
        self.is_second_player_cached = False
        self.second_player_cache = None

        self.board = np.empty(
            shape=(Board.MIN_ROWS, Board.MIN_COLUMNS),
            dtype=object
        )
        self.move_history = []
        self.player1 = None
        self.player2 = None
        self.player_just_played = None
        self.output_is_enabled = True

    def create(self, player1, player2, rows, columns, do_output=False):
        if (columns < Board.MIN_COLUMNS or rows < Board.MIN_ROWS):
            raise Exception("Provided board size is too small")

        self.rows = rows
        self.columns = columns

        self.board = np.empty(
            shape=(self.rows, self.columns),
            dtype=object
        )

        self.player1 = player1
        self.player2 = player2

        row = 0
        column = 0

        for _ in range(12):
            new_piece = bp.BoardPiece(
                self,
                row,
                column,
                be.BoardElement.player1
            )
            self.first_player_pieces.append(new_piece)
            self.set_bitmap(row, column, new_piece)

            column += 1

            if column > 4:
                column -= 5
                row += 1

        # Skip middle field
        column += 1

        for _ in range(12):
            new_piece = bp.BoardPiece(
                self,
                row,
                column,
                be.BoardElement.player2
            )
            self.second_player_pieces.append(new_piece)
            self.set_bitmap(row, column, new_piece)

            column += 1

            if column > 4:
                column -= 5
                row += 1

    def set_bitmap(self, row, column, value):
        self.board[row, column] = value

    def is_free(self, row, column):
        if row < 0 or row >= 5:
            return False

        if column < 0 or column >= 5:
            return False

        if self.board[row, column]:
            return False

        return True

    def get_piece(self, row, column):
        return self.board[row, column]

    def apply_action(self, action):
        if action.type_ != a.Action.ACTION_UNDO:
            self.move_history.append(action)

        source_row, source_column = action.source
        destination_row, destination_column = action.destination

        piece = self.get_piece(source_row, source_column)

        if piece is None:
            raise Exception("No piece for given source found!")

        piece.move(destination_row, destination_column)

        if action.type_ == a.Action.ACTION_CAPTURE:
            captured_piece = action.captured
            captured_piece.captured()

            if captured_piece.board_element == be.BoardElement.player2:
                self.second_player_pieces.remove(captured_piece)

            else:
                self.first_player_pieces.remove(captured_piece)

        elif action.type_ == a.Action.ACTION_UNDO:
            captured_piece = action.captured

            if captured_piece is not None:
                self.set_bitmap(
                    captured_piece.position[0],
                    captured_piece.position[1],
                    captured_piece
                )

                if captured_piece.board_element == be.BoardElement.player2:
                    self.second_player_pieces.append(captured_piece)

                else:
                    self.first_player_pieces.append(captured_piece)

        self.is_first_player_cached = False
        self.is_second_player_cached = False

    def all_moves_for_player(self, board_element):
        # print "Getting all moves for player {0}".format(board_element)

        if board_element == be.BoardElement.player1:
            if self.is_first_player_cached:
                return self.first_player_cache

        else:
            if self.is_second_player_cached:
                return self.second_player_cache

        moves = []
        can_capture = False

        if board_element == be.BoardElement.player2:
            for piece in self.second_player_pieces:
                possible_actions = piece.possible_action()
                # print "Piece {0} for second_player: Actions {1}".format(piece.position, possible_actions)
                moves = moves + possible_actions

        else:
            for piece in self.first_player_pieces:
                moves = moves + piece.possible_action()

        for move in moves:
            if move.type_ == a.Action.ACTION_CAPTURE:
                can_capture = True
                break

        if can_capture:
            new_moves = []

            for move in moves:
                if move.type_ == a.Action.ACTION_CAPTURE:
                    new_moves.append(move)

            moves = new_moves

        if board_element == be.BoardElement.player1:
            self.first_player_cache = moves
            self.is_first_player_cached = True

        else:
            self.second_player_cache = moves
            self.is_second_player_cached = True

        return moves

    def score(self, weights):
        player1_weights = {
            be.BoardElement.piece: 0,
            be.BoardElement.back: 0,
            be.BoardElement.center: 0,
            be.BoardElement.front: 0,
        }
        player2_weights = player1_weights.copy()

        for piece in self.first_player_pieces:
            features = bp.BoardPiece.get_features(piece)

            for feature in features:
                player1_weights[feature] += 1

        player1_score  = sum(
            [player1_weights[key] * weights[key] for key in weights.keys()]
        )

        for piece in self.second_player_pieces:
            features = bp.BoardPiece.get_features(piece)

            for feature in features:
                player2_weights[feature] += 1

        player2_score  = sum(
            [player2_weights[key] * weights[key] for key in weights.keys()]
        )

        return player1_score - player2_score

    def undo_last_action(self):
        last_action = self.move_history.pop()
        undo_action = last_action.undo()
        self.apply_action(undo_action)

    def __str__(self):
        string = ""

        for row in range(self.rows):
            for column in range(self.columns):
                piece = self.board[row, column]

                if piece is None:
                    string += '{0} '.format(be.BoardElement.neutral_symbol)

                elif piece.board_element == be.BoardElement.player1:
                    string += '{0} '.format(be.BoardElement.player1_symbol)

                else:
                    string += '{0} '.format(be.BoardElement.player2_symbol)

            string += '\n'

        return string
