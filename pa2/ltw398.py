# File: Player.py
# Author(s) names AND netid's: 
#       Yuqing Chen,    yco664
#       Lijun Tang,     ltw398
#       Sisi Chen,      sci963
# Date: 2015/4/13
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.



from random import *
from decimal import *
from copy import *
from MancalaBoard import *
from math import sqrt

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    ABPRUNEBONUS = 5
    
    def __init__(self, playerNum, playerType, ply=0):     #change ply here
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #print "inside ply == 0"
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            # why the same type
            opp = Player(self.opp, self.type, self.ply)
            # why ply-1
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.


    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        turn = self
        r = self.alphabeta(board, ply, turn, -INFINITY, INFINITY, True, -1)         # call the helper function, return a (score, move) tuple
        return (r[0], r[1])             # r[0] = score, r[1] = move
    
    def alphabeta(self, board, ply, turn, alpha, beta, Player_Max, move):
        """ Helper function """
        if ply == 0 or board.gameOver():
            return (turn.score(board), move)
        if Player_Max:      #The node is max
            score = -INFINITY
            for m in board.legalMoves(self):
            #for each legal move
                nb = deepcopy(board)
                nb.makeMove(self, m)
                opp = Player(self.opp, self.type, self.ply)
                r1 = opp.alphabeta(nb, ply-1, turn, alpha, beta, False, move)
                score = max(score, r1[0])
                if alpha < score:
                    alpha = score
                    move = m
                if beta <= alpha:
                    #print "beta pruning"
                    break   #beta pruning
                #print "Min"
            return (score, move)
        else:      #The node is min
            score = INFINITY
            for m in board.legalMoves(self):
            #for each legal move
                nb = deepcopy(board)
                nb.makeMove(self, m)
                opp = Player(self.opp, self.type, self.ply)
                r2 = opp.alphabeta(nb, ply-1, turn, alpha, beta, True, move)
                score = min(score, r2[0])
                if beta > score:
                    beta = score
                    move = m
                if beta <= alpha:
                   # print "alpha pruning"
                    break   #alpha pruning
                #print "Max"
            return (score, move)
        
                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            val, move = self.bestMove(board, self.ply)
            #val, move = self.alphaBetaMoveBonus(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNEBONUS:
            val, move = self.alphaBetaMoveBonus(board, self.ply)
            print "chose move", move, " with value", val
            return move

        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class ltw398(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        #print "Calling score in MancalaPlayer"         #modified
        mancala_stones = board.scoreCups[self.num - 1]      #s tones in the player side mancala
        cups = board.getPlayersCups(self.num)           # the player side cups
        empty_cups = 0                  # the number of empty cups
        cups_stones = 0                 # total number of stones in the player side cups
        danger_stones = 0

        total_stone = 0

        opp_cup = board.getPlayersCups(self.opp)

        delta = 0

        for i in range(6):
            delta += (cups[i] - (6 - i)) ** 2

        delta = sqrt(delta)

        for elem in cups:
            cups_stones += elem
            if elem == 0:
                empty_cups += 1

        for i in range(6):
            if opp_cup[i] == 0:
                danger_stones += cups[5-i]

        #for elem in opp_cup:
            #total_stone += elem

        #total_stone += cups_stones

        #total_stone_weight = (48 - total_stone + 20) / 48

        #score = 2 * mancala_stones + 0.65 * cups_stones + 1 * empty_cups - 0.2 * delta
        score = 2 * mancala_stones + 0.65 * cups_stones + 1 * empty_cups - 0.2 * delta - 0.1 * danger_stones
        #score = 2 * mancala_stones + 0.65 * total_stone_weight * cups_stones + 1 * empty_cups - 0.2 * delta
        #print "score =", score
        return score

    def bestMove(self, board, ply):
        """customized best move, return (score, move)"""
        # first hard coded case: if we have a move that can play again, make it
        cups = board.getPlayersCups(self.num)     # our side cups
        opps = board.getPlayersCups(self.opp)    # opps side cups
        for i in range (6):      # i from 0 to 5
            if cups[6-i-1] == i+1:          # first check whether cup 6 has 1 stone, etc
                return (-1, 6-i)        # score = -1
        
        # second hard coded case: if we can collect opponent's stones by landing the last stone in one of our empty cup in a move, make it
        empty = []         # store the index of empty cups in our side
        nonempty = []           # store the index of non-empty cups in our side
        bonus = 0           # bonus we gained
        move = -1
        score = 0
        for i in range (6):
            if cups[i] == 0:
                empty.append(i)
            else:
                nonempty.append(i)
        for a in empty:             # a is a index of empty cup
            for b in nonempty:              # b is a index of nonempty cup
                if b < a:                   # b is on the left of a
                    if cups[b] == a-b:          # the number of stones in b can land the last stone at a 
                            temp_bonus = opps[5-a] + 1
                            
                            # TODO: need to consider when they are equal, which one to choose, leftmost or rightmost
                            
                            if temp_bonus > bonus:          # if we get a larger bonus, update the move
                                bonus = temp_bonus
                                move = b+1
                                score = self.alphaBetaMove(board, 5)
                            elif temp_bonus == bonus:
                                temp_score = self.alphaBetaMove(board, 5)
                                if temp_score > score:
                                    move = b +1
                                    score = temp_score

                                #print move
                    elif cups[b] == 13:         # the number of stones in b can land the last stone at b with loop
                        
                        # TODO: need to consider the stones we give to opps : temp_bonus = 3+opps[5-b]-5
                        temp_bonus = 3+opps[5-b]    # 3 comes from 1 in cups[b], 1 in our mancala and 1 in opps[5-b] that we add
                        
                        if temp_bonus > bonus:          # if we get a larger bonus, update the move
                            bonus = temp_bonus
                            move = b+1
                            score = self.alphaBetaMove(board, 5)
                        elif temp_bonus == bonus:
                            temp_score = self.alphaBetaMove(board, 5)
                            if temp_score > score:
                                move = b +1
                                score = temp_score
                            #print move
                if b > a:
                    if cups[b] == 13 - (b - a):             # the last stone of b lands on cup a
                        temp_bonus = 3 + opps[5-a]
                        if temp_bonus > bonus:          # if we get a larger bonus, update the move
                            bonus = temp_bonus
                            move = b+1
                            score = self.alphaBetaMove(board, 5)
                        elif temp_bonus == bonus:
                            temp_score = self.alphaBetaMove(board, 5)
                            if temp_score > score:
                                move = b +1
                                score = temp_score
                            #print move
                    elif cups[b] == 13:
                        temp_bonus = 3+opps[5-b]
                        if temp_bonus > bonus:          # if we get a larger bonus, update the move
                            bonus = temp_bonus
                            move = b+1
                            score = self.alphaBetaMove(board, 5)
                        elif temp_bonus == bonus:
                            temp_score = self.alphaBetaMove(board, 5)
                            if temp_score > score:
                                move = b +1
                                score = temp_score
                            #print move
        if bonus != 0:              # if there is no case we can get bonus out of it
            return (-1, move)                   # return the move with largest bonus

        # third case
        return self.alphaBetaMoveBonus(board, 8)     # set ply = 5

    def alphaBetaMoveBonus(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        print "inside alphaBetaMoveBonus"
        turn = self
        r = self.alphabetaBonus(board, ply, turn, -INFINITY, INFINITY, True, -1)         # call the helper function, return a (score, move) tuple
        return (r[0], r[1])             # r[0] = score, r[1] = move
    
    def alphabetaBonus(self, board, ply, turn, alpha, beta, Player_Max, move):
        """ Helper function """
    
        if ply == 0 or board.gameOver():
            return (turn.score(board), move)
        if Player_Max:      #The node is max
            score = -INFINITY
            for m in board.legalMoves(self):
            #for each legal move
                nb = deepcopy(board)
                #make a new board
                playAgain = nb.makeMove(self, m)
                
                r1 = ()
                if playAgain:
                    #print "inside max true"
                    r1 = self.alphabetaBonus(nb, ply, turn, alpha, beta, True, move)
                #try the move
                else:
                    #print "inside max false"
                    opp = ltw398(self.opp, self.type, self.ply)
                    r1 = opp.alphabetaBonus(nb, ply-1, turn, alpha, beta, False, move)

                score = max(score, r1[0])
                if alpha < score:
                    alpha = score
                    move = m
                if beta <= alpha:
                    #print "beta pruning"
                    break   #beta pruning
                #print "Min"
            return (score, move)
        else:      #The node is min
            score = INFINITY
            for m in board.legalMoves(self):
            #for each legal move
                nb = deepcopy(board)
                #make a new board
                playAgain = nb.makeMove(self, m)
                #try the move
                r2 = ()

                if playAgain:
                    #print "inside min false"
                    r2 = self.alphabetaBonus(nb, ply, turn, alpha, beta, False, move)

                else:
                    #print "inside max true"
                    opp = ltw398(self.opp, self.type, self.ply)
                    r2 = opp.alphabetaBonus(nb, ply-1, turn, alpha, beta, True, move)

                score = min(score, r2[0])
                if beta > score:
                    beta = score
                    move = m
                if beta <= alpha:
                   # print "alpha pruning"
                    break   #alpha pruning
                #print "Max"
            return (score, move)
     
