#!/usr/bin/env python
# weights.py module
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
import board_element as be

weights_aggressive = {
    be.BoardElement.piece: 400,
    be.BoardElement.back: 10,
    be.BoardElement.center: 30,
    be.BoardElement.front: 60,
}
weights_neutral = {
    be.BoardElement.piece: 0,
    be.BoardElement.back: 0,
    be.BoardElement.center: 0,
    be.BoardElement.front: 0,
}
weights_front = {
    be.BoardElement.piece: 200,
    be.BoardElement.back: 10,
    be.BoardElement.center: 30,
    be.BoardElement.front: 600,
}
