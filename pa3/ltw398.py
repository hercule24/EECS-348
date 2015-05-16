#!/usr/bin/env python
import struct, string, math

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
                                                                  
                                                                  
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)


    
class FC_Solver:
    def __init__(self, K):
        # rowValid[i][j] means that in ith row, number j is used
        self.K = K

        self.rowValid = []
        for i in range(K):
            row = [0] * (K + 1)
            self.rowValid.append(row)
        
        # columnValid[i][j] means that in ith column, number j is used.
        self.columnValid = []
        for i in range(K):
            col = [0] * (K + 1)
            self.columnValid.append(col)
        
        # subBoardValid[i][j] means that in ith subBoard, number j is used
        self.subBoardValid = []
        for i in range(K):
            cell = [0] * (K + 1)
            self.subBoardValid.append(cell)

    def fill(self, row, col, val):
        sqrt = int(math.sqrt(self.K))
        #print self.rowValid
        self.rowValid[row][val] = 1
        #print "inside fill rowValid =", self.rowValid
        self.columnValid[col][val] = 1
        self.subBoardValid[(row/sqrt)*sqrt+col/sqrt][val] = 1

    def isValid(self, row, col, val):
        sqrt = int(math.sqrt(self.K))
        #print "inside isValid"
        #print "val =", val
        #print "row =", row
        #print "col =", col
        #if val == 3:
            #print self.rowValid
            #print self.columnValid
            #print self.subBoardValid
        if self.rowValid[row][val] == 0 and self.columnValid[col][val] == 0 and self.subBoardValid[(row/sqrt)*sqrt+col/sqrt][val] == 0:
            #print "val = %d, valid!" % val
            return True
        else:
            #print "val = %d, not valid!" % val
            return False

    def clear(self, row, col, val):
        sqrt = int(math.sqrt(self.K))
        self.rowValid[row][val] = 0
        self.columnValid[col][val] = 0
        self.subBoardValid[(row/sqrt)*sqrt+col/sqrt][val] = 0

    def solveSudoku(self, board):
        #print "****************"
        #print self.rowValid
        #print self.columnValid
        #print self.subBoardValid
        #print "****************"
        for i in range(self.K):
            for j in range(self.K):
                #print "board[%d][%d] = %d" % (i, j, board[i][j])
                if board[i][j] != 0:
                    self.fill(i, j, board[i][j])
                #print "rowValid =", self.rowValid

        #print "****************"
        #print self.rowValid
        #print self.columnValid
        #print self.subBoardValid
        #print "****************"

        if self.solver(board, 0):
            #print "solved"
            #print board
            return board

    def solver(self, board, index):
        #print board
        if index == self.K * self.K:
            return True

        row = index / self.K
        col = index - self.K * row
        #print "row =", row
        #print "col =", col

        if board[row][col] != 0:
            #print "inside != 0"
            return self.solver(board, index+1)

        for val in range(1, (self.K)+1):
            #print "inside for"
            if self.isValid(row, col, val):
                #print "row =", row
                #print "col =", col
                board[row][col] = val
                #print board
                #print
                self.fill(row, col, val)
                if self.solver(board, index+1):
                    return True
                else:
                    self.clear(row, col, val)

        board[row][col] = 0
        return False

def solve(initial_board, forward_checking = False, MRV = False, MCV = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    if forward_checking:
        board = initial_board.CurrentGameBoard
        K = len(board)
        solver = FC_Solver(K)
        solved_board = solver.solveSudoku(board)
        solved_board = SudokuBoard(K, solved_board)
        return solved_board
