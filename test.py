#!/usr/bin/env python
# test.py module
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
import controller.controller    as c
import controller.weights       as w
import controller.game_states   as gs


def main():
    controller = c.Controller(
        number_of_rows=5,
        number_of_columns=5,
        weights=w.weights_aggressive,
        barrier=5,
        verbose=True
    )
    controller.play()

    if controller.winner == gs.GameStates.STATE_DRAW:
        print "Oh noes, no winner :'( We've got a DRAW!"

    else:
        print "Yay, we got a winner! Winner is player no. {0}!".format(
            controller.winner
        )

if __name__ == "__main__":
    main()
