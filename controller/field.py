#!/usr/bin/env python
# field.py module
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


class Field(object):
    def __init__(self, line=0, row=0):
        self.line = line
        self.row = row

    def is_inside_board(self, board_interface):
        return (self.line >= 0
                and
                self.row >= 0
                and
                self.line < board_interface.number_of_lines()
                and
                self.row < board_interface.number_of_rows()
                )

    def print_(self):
        print "[{0},{1}]".format(self.row, self.line)

    def is_equal_to(self, field):
        return self.line == field.line and self.row == field.row
