#!/usr/bin/env python
import struct, string, math, operator
from collections import namedtuple

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

class Solver:
    """Implement BC, FC, MRV, MCV and LCV"""
    def __init__(self, K, FC, MRV, MCV, LCV):
        self.K = K
        # count keeps track of the number of variable assignments
        self.count = 0
        self.FC = FC
        self.MRV = MRV
        self.MCV = MCV
        self.LCV = LCV
        # rowValid[i][j] means that in ith row, number j is used
        self.rowValid = []
        for i in range(K):
            row = [0] * (K + 1)
            self.rowValid.append(row)
         # columnValid[i][j] means that in ith column, number j is used
        self.columnValid = []
        for i in range(K):
            col = [0] * (K + 1)
            self.columnValid.append(col)

         # subBoardValid[i][j] means that in ith subBoard, number j is used
        self.subBoardValid = []
        for i in range(K):
            cell = [0] * (K + 1)
            self.subBoardValid.append(cell)

        # initailize a namedtuple called Index    
        self.Index = namedtuple("Index",["row","col"])

    def MRV_remain_num(self, row, col):
        """calculate the number of remaining values for board[row][col]"""
        remainNum = 0
        for val in range(1, self.K + 1):
            if self.isValid(row, col, val):
                remainNum += 1
        return remainNum

    def MCV_empty_num(self, board, row, col):
        """calculate the number of constraints for board[row][col]"""
        emptyNum = 0
        for i in range(self.K):
            if board[row][i] == 0 and i != col:
                emptyNum += 1
        for i in range(self.K):
            if board[i][col] == 0 and i != row:
                emptyNum += 1

        subsquare = int(math.sqrt(self.K))
        SquareRow = row // subsquare
        SquareCol = col // subsquare
        for i in range(subsquare):
             for j in range(subsquare):
                r = SquareRow*subsquare+i
                c = SquareCol*subsquare+j
                if r != row and c != col and board[r][c] == 0:
                    emptyNum += 1
        return emptyNum

    def LCV_neighbor_valid_num(self, board, row, col, val):
        """find out the number of availale neighbors with the given value"""
        neighborNum = 0
        for i in range(self.K):
            if board[row][i] == 0 and i != col:
                if self.isValid(row, i, val):
                    neighborNum += 1
        for i in range(self.K):
            if board[i][col] == 0 and i != row:
                if self.isValid(i, col, val):
                    neighborNum += 1
        subsquare = int(math.sqrt(self.K))
        SquareRow = row // subsquare
        SquareCol = col // subsquare
        for i in range(subsquare):
             for j in range(subsquare):
                r = SquareRow*subsquare+i
                c = SquareCol*subsquare+j
                if r != row and c != col and board[r][c] == 0:
                    if self.isValid(r, c, val):
                        neighborNum += 1
        return neighborNum

    def findMCV(self, board):
        """find out the position of MCV"""
        MCV_dic = {}
        for r in range(self.K):
            for c in range(self.K):
                if board[r][c] == 0:
                    emptyNum = self.MCV_empty_num(board, r, c)
                    i = self.Index(row = r, col = c)
                    MCV_dic[i] = emptyNum
        MCV_list = list(reversed(sorted(MCV_dic.items(), key = operator.itemgetter(1))))
        return MCV_list 

    def findMRV(self, board):
        """find out the position of MRV"""
        MRV_dic = {}
        for r in range(self.K):
            for c in range(self.K):
                if board[r][c] == 0:
                    remainNum = self.MRV_remain_num(r, c)
                    i = self.Index(row = r, col = c)
                    MRV_dic[i] = remainNum
        MRV_list = sorted(MRV_dic.items(), key = operator.itemgetter(1))
        # print MRV_list
        # print MRV_list[0][0]
        return MRV_list

    def findLCV(self, board, row, col):
        """find the value with LCV"""
        LCV_dic = {}
        for val in range(1,self.K + 1):
            if self.isValid(row, col, val):
                LCV_dic[val] = self.LCV_neighbor_valid_num(board, row, col, val)
        LCV_list = sorted(LCV_dic.items(), key = operator.itemgetter(1))
        return LCV_list


    def fill(self, row, col, val):
        """Set corresponding elements from 0 to 1 in rowValid, columnValid and subBoardValid"""
        sqrt = int(math.sqrt(self.K))
        self.rowValid[row][val] = 1
        self.columnValid[col][val] = 1
        self.subBoardValid[(row // sqrt) * sqrt + col // sqrt][val] = 1
    def isValid(self, row, col, val):
        """Return Ture if val is not in the corresponding row, col or subBoard, False otherwise"""
        sqrt = int(math.sqrt(self.K))
        if self.rowValid[row][val] == 0 and self.columnValid[col][val] == 0 and self.subBoardValid[(row // sqrt) * sqrt + col // sqrt][val] == 0:
            return True
        else:
            return False

    def clear(self, row, col, val):
        """Reset val from 1 to 0 in rowValid, columnValid, and subBoardValid"""
        sqrt = int(math.sqrt(self.K))
        self.rowValid[row][val] = 0
        self.columnValid[col][val] = 0
        self.subBoardValid[(row // sqrt) * sqrt + col // sqrt][val] = 0

    def forward_checking(self, board, row, col):
        """Check whether there exists a unassigned variable has an empty domain.
        Return False when there exists such variables, True otherwise"""
        # check the unassigned variables in the same row
        flag = 0
        for i in range(self.K):
            if board[row][i] == 0:
                for val in range(1, self.K + 1):
                    if self.isValid(row, i, val):
                        flag = 1
                        break
                if flag == 0:
                    return False

        # check the unassigned variables in the same col
        flag = 0
        for i in range(self.K):
            if board[i][col] == 0:
                for val in range(1, self.K + 1):
                    if self.isValid(i, col, val):
                        flag = 1
                        break
                if flag == 0:
                    return False
                    
        # check the unassigned variables in the same subBoard
        flag = 0
        subsquare = int(math.sqrt(self.K))
        SquareRow = row // subsquare
        SquareCol = col // subsquare
        for i in range(subsquare):
             for j in range(subsquare):
                r = SquareRow*subsquare+i
                c = SquareCol*subsquare+j
                if r != row and c != col and board[r][c] == 0:
                    for val in range(1, self.K +1):
                       if self.isValid(r, c, val):
                            flag = 1
                            break
                    if flag == 0:
                        return False
        return True
    
    def findMRV_MCV(self, board):
        """ Combine MRV and MCV with MCV acting as a tie breaker for MRV"""
        MRV_list = self.findMRV(board)
        if MRV_list == []:
            return MRV_list
        mini = MRV_list[0][1]
        same_min_list = []
        for item in MRV_list:
            if item[1] == mini:
                same_min_list.append(item[0])
            else:
                break
        MRV_MCV_dic = {} 
        for elem in same_min_list:
            emptyNum = self.MCV_empty_num(board, elem.row, elem.col)
            MRV_MCV_dic[elem] = emptyNum
        MRV_MCV_list = list(reversed(sorted(MRV_MCV_dic.items(), key = operator.itemgetter(1))))
        return MRV_MCV_list 
        

    def solveSudoku(self, board):
        """Set rowValid, columnValid and subBoardValid correctly for board and return solved board if success"""
        for i in range(self.K):
            for j in range(self.K):
                if board[i][j] != 0:
                    self.fill(i, j, board[i][j])

        if self.solver(board, 0):
            return board

    def solver(self, board, index):
        """Return True if successfully solve the board, False otherwise. Set the board as well"""
        
        # If both MCV and MRV are True, then use MCV as a tie breaker for MRV to assign new values
        if self.MCV and self.MRV:
            i = self.findMRV_MCV(board)
            if i == []:
                return True
            else:
                row = i[0][0].row
                col = i[0][0].col

        # If only MCV is True, then choose the MRV to assign new values
        elif self.MCV:
            i = self.findMCV(board)
            if i == []:
                return True
            else:
                row = i[0][0].row
                col = i[0][0].col
        # If only MRV is True, then choose the MRV to assign new values
        elif self.MRV:
            i = self.findMRV(board)
            if i == []:
                return True
            else:
                row = i[0][0].row
                col = i[0][0].col
        else:

            # If MRV and MCV are both False, then compute row and col in serial
            row = index // self.K
            col = index - row * self.K
            if index == self.K * self.K:
                return True

        if board[row][col] != 0:
            return self.solver(board, index + 1)
        # If LCV is True, then choose the LCV 
        if self.LCV:
            val = self.findLCV(board, row, col)
            if val == []:
                return False
                #increase count of variable assignments
            else: 
                for v in val:
                     self.count = self.count + 1
                     v = v[0]
                     board[row][col] = v
                     self.fill(row, col, v)
        
            # If forward_checking is True, then perform forward checking with backtracking
                     if self.FC == True:
                        if not self.forward_checking(board, row, col):
                            self.clear(row, col, v)
                            continue
            # If forward_checking is False, then only perform backtracking
                     if self.solver(board, index + 1):
                        return True
                     else:
                        self.clear(row, col, v)


            board[row][col] = 0
            return False
        else:

            for val in range(1, self.K + 1):
                 if self.isValid(row, col, val):
                    #increase count of variable assignments
                    self.count = self.count + 1
                    board[row][col] = val
                    self.fill(row, col, val)
                    
                    # If forward_checking is True, then perform forward checking with backtracking
                    if self.FC == True:
                        if not self.forward_checking(board, row, col):
                            self.clear(row, col, val)
                            continue
                    # If forward_checking is False, then only perform backtracking
                    if self.solver(board, index + 1):
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
    board = initial_board.CurrentGameBoard
    K = len(board)
    solver = Solver(K, forward_checking, MRV, MCV, LCV)
    solved_board = solver.solveSudoku(board)
    solved_board = SudokuBoard(K, solved_board)
    print solver.count
    return solved_board
