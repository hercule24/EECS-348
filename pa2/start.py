#!/usr/bin/python

from MancalaGUI import *
#from Player import * 
#from MancalaBoard import *
from TicTacToe import *

def start(p2):
    p1 = Player(1, Player.HUMAN)
    startGame(p1, p2)

if __name__ == "__main__":
    print "Select the Game Mode!"
    print "1. Play with your friend"
    print "2. Play against a random player"
    print "3. Play against a minimax player"
    print "4. Play against a abprune player"
    print "5. Play against a customized player"
    print "6. Play a tic tac toe using minimax"
    print "7. Play a tic tac toe using abprune"
    print "8. Play mancala using abprune, against our customized"
    print "9. Play against a CUSTOM, with human as second"
    print "10.Play against a abprune against abprunebonus"
    print "11.Play against a ABPRUNEBONUS against CUSTOM"
    print "12.Play against a CUSTOM against HUMAN"

    while True:
        input = int(raw_input("Please select a mode: "))
        if input == 1:
            p2 = ltw398(2, Player.HUMAN)
            start(p2)

        elif input == 2:
            p2 = ltw398(2, Player.RANDOM)
            start(p2)

        elif input == 3:
            p2 = ltw398(2, Player.MINIMAX, 5)
            start(p2)

        elif input == 4:
            p2 = ltw398(2, Player.ABPRUNE, 5)
            start(p2)

        elif input == 5:
            p2 = ltw398(2, Player.CUSTOM)
            start(p2)

        elif input == 6:
            p1 = Player(1, Player.HUMAN)
            p2 = Player(2, Player.MINIMAX, 9)
            b = TTTBoard()
            b.hostGame(p1, p2)

        elif input == 7:
            p1 = Player(1, Player.HUMAN)
            p2 = Player(2, Player.ABPRUNE, 9)
            b = TTTBoard()
            b.hostGame(p1, p2)

        elif input == 8:
            p1 = ltw398(1, Player.ABPRUNE, 9)
            p2 = ltw398(2, Player.CUSTOM)
            startGame(p1, p2)

        elif input == 9:
            p1 = ltw398(1, Player.MINIMAX, 5)
            p2 = ltw398(2, Player.HUMAN)
            startGame(p1, p2)

        elif input == 10:
            p1 = ltw398(1, Player.ABPRUNE, 9)
            p2 = ltw398(2, Player.ABPRUNEBONUS, 9)
            startGame(p1, p2)

        elif input == 11:
            p2 = ltw398(2, Player.ABPRUNEBONUS, 9)
            p1 = ltw398(1, Player.CUSTOM)
            startGame(p1, p2)
        
        elif input == 12:
            p1 = ltw398(1, Player.CUSTOM)
            p2 = ltw398(2, Player.HUMAN)
            startGame(p1, p2)

        else:
            print "Mode not found, please reselect!"
