#!/usr/bin/env python
# action.py module
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Thi Thuy-Duc Dao (daodt1@bfh.ch), Sven Osterwalder (ostes2@bfh.ch)
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


class Action(object):
    ACTION_UNDO = 'UNDO'
    ACTION_MOVE = 'MOVE'
    ACTION_CAPTURE = 'CAPTURE'

    def __init__(
        self,
        action_type,
        source,
        destination,
        captured=None,
    ):
        self.type_ = action_type
        self.source = source
        self.destination = destination
        self.captured = captured

    def undo(self):
        return Action(
            self.ACTION_UNDO,
            self.destination,
            self.source,
            self.captured,
        )

    def copy(self):
        return Action(
            self.type_,
            self.source,
            self.destination,
            self.captured,
        )

    def __len__(self):
        return 1

    def __eq__(self, other):
        if other is None:
            return False

        if self.type_ != other.type_:
            return False

        if self.source != other.source:
            return False

        if self.destination != other.destination:
            return False

        if self.captured != other.captured:
            return False

        return True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{0} :: <{1}, {2}> -> <{3}, {4}>".format(
            self.type_,
            self.source[0],
            self.source[1],
            self.destination[0],
            self.destination[1]
        )
