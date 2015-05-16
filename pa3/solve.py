#!/usr/bin/python
import time
from yco664 import *

if __name__ == "__main__":
    print "Select the combination!"
    print " 0: BT"
    print " 1: BT + FC"
    print " 2: BT + MRV"
    print " 3: BT + MCV"
    print " 4: BT + LCV"
    print " 5: BT + FC + MRV"
    print " 6: BT + FC + MCV"
    print " 7: BT + MCV + MRV"
    print " 8: BT + FC + LCV"
    print " 9: BT + FC + MRV + LCV"
    print " 10: BT + FC + MCV + LCV"
    print " 11: BT + FC + MRV + MCV + LCV"
    print " 12: BT + FC + MRV + MCV"
    
    input = int(raw_input("Please select a combination: "))
    
    print "Select your board"
    print "0: 4*4 easy"
    print "1: 9*9 easy"
    print "2: 16*16 easy"
    print "3: 25*25 easy"
    print "4: 9*9 more"
    print "5: 16*16 more"
    print "6: 25*25 more"

    b = int(raw_input("Please select a board: "))
    if b == 0:
        sb = init_board("input_puzzles/easy/4_4.sudoku")
    elif b == 1:
        sb = init_board("input_puzzles/easy/9_9.sudoku")
    elif b == 2:
        sb = init_board("input_puzzles/easy/16_16.sudoku")
    elif b == 3:
        sb = init_board("input_puzzles/easy/25_25.sudoku")
    elif b == 4:
        sb = init_board("input_puzzles/more/9x9/9x9.1.sudoku")
    elif b == 5:
        sb = init_board("input_puzzles/more/16x16/16x16.1.sudoku")
    elif b == 6:
        sb = init_board("input_puzzles/more/25x25/25x25.1.sudoku")
    
    print "initial board"
    sb.print_board()
    start_time = time.time()
    if input == 0:
        fb = solve(sb, False, False, False, False)
    elif input == 1:
        fb = solve(sb, True, False, False, False)
    elif input == 2:
        fb = solve(sb, False, True, False, False)
    elif input == 3:
        fb = solve(sb, False, False, True, False)
    elif input == 4:
        fb = solve(sb, False, False, False, True)
    elif input == 5:
        fb = solve(sb, True, True, False, False)
    elif input == 6:
        fb = solve(sb, True, False, True, False)
    elif input == 7:
        fb = solve(sb, False, True, True, False)
    elif input == 8:
        fb = solve(sb, True, False, False, True)
    elif input == 9:
        fb = solve(sb, True, True, False, True)
    elif input == 10:
        fb = solve(sb, True, False, True, True)
    elif input == 11:
        fb = solve(sb, True, True, True, True)
    elif input == 12:
        fb = solve(sb, True, True, True, False)
    print "solved board"
    fb.print_board()
    print("You spend %s seconds" % (time.time() - start_time))
    if is_complete(fb):
        print "complete!"
