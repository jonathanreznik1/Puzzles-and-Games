# Adapted code from:
# https://www.geeksforgeeks.org/n-queen-problem-backtracking-3/?ref=lbp
#   -Changed function parameters mostly to allow outside board object 

# Python3 program to solve N Queen
# Problem using backtracking
DEBUG = False
# global N
# N = 4


# def board_solve(arg):
#     if arg == 1:
#         board_solved_backtracking(self)
#     elif arg == 2:
#         board_solved_bruteforce(self)

def board_solved_backtracking(self):
    return False

def board_solved_brute(self):
    # O(n) algorithm for rows
    for row in games[self.b_id]:
        if [x.has_piece() for x in row].count(True) > 1:
            print("unsolved - row with 2 pieces")
            return False
    # Algorithm for columns
    for i in range(len(games[self.b_id])):
        if [col[i].has_piece() for col in games[self.b_id]].count(True) > 1:
            print("unsolved - col with 2 pieces")
            return False

def checkdiagonals():
# Algorithm to check diagonals
    # for a in [0,1,2,3]:
    #     if [board[i+1][i].has_piece() for i in range(len(board))].count(True) > 1:
    #         print("unsolved - diagonal with 2 pieces on it")
    #     return False
    # for a,b in [(0,0),(1,0),(0,1),(2,0),(0,2),(3,0),(0,3)]:
    #     if [board[i+a][i+b].has_piece() for i in range(len(board))].count(True) > 1:
    #         print("unsolved - diagonal with 2 pieces on it")
    #     return False
    return True



def printSolution(board):
    if DEBUG:
        print("printSolution called from helper module Solutions.py")
        for i in range(len(board)):
            for j in range(len(board)):
                print(board[i][j], end = " ")
        print(board)


# A utility function to check if a queen can
# be placed on board[row][col]. Note that this
# function is called when "col" queens are
# already placed in columns from 0 to col -1.
# So we need to check only left side for
# attacking queens
def isSafe(board, row, col):
    # Check this row on left side
    for i in range(col):
        if board[row][i].has_piece():
            return False

    # Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board[i][j].has_piece():
            return False

    # Check lower diagonal on left side
    for i, j in zip(range(row, len(board), 1),
                    range(col, -1, -1)):
        if board[i][j].has_piece():
            return False

    return True

def solveNQUtil(board, col):
    
    # base case: If all queens are placed
    # then return true
    if col >= len(board):
        return True

    # Consider this column and try placing
    # this queen in all rows one by one
    for i in range(len(board)):

        if isSafe(board, i, col):
            
            # Place this queen in board[i][col]
            board[i][col].set_piece("Qu")

            # recur to place rest of the queens
            if solveNQUtil(board, col + 1) == True:
                return True

            # If placing queen in board[i][col
            # doesn't lead to a solution, then
            # queen from board[i][col]
            board[i][col].reset_square()

    # if the queen can not be placed in any row in
    # this column col then return false
    return False

# This function solves the N Queen problem using
# Backtracking. It mainly uses solveNQUtil() to
# solve the problem. It returns false if queens
# cannot be placed, otherwise return true and
# placement of queens in the form of 1s.
# note that there may be more than one
# solutions, this function prints one of the
# feasible solutions.
def solveNQ(board):
    # board = [ [0, 0, 0, 0],
    # 		[0, 0, 0, 0],
    # 		[0, 0, 0, 0],
    # 		[0, 0, 0, 0] ]

    if solveNQUtil(board, 0) == False:
        print ("Solution does not exist")
        return False

    if DEBUG:
        print("board is solved")
    printSolution(board)
    return True

# Driver Code
# solveNQ()

# # This code is contributed by Divyanshu Mehta



# """ Python3 program to solve N Queen Problem using
# backtracking """
# N = 4

# """ ld is an array where its indices indicate row-col+N-1
# (N-1) is for shifting the difference to store negative
# indices """
# ld = [0] * 30

# """ rd is an array where its indices indicate row+col
# and used to check whether a queen can be placed on
# right diagonal or not"""
# rd = [0] * 30

# """column array where its indices indicates column and
# used to check whether a queen can be placed in that
# 	row or not"""
# cl = [0] * 30

# """ A utility function to print solution """
# def printSolution(board):
# 	for i in range(N):
# 		for j in range(N):
# 			print(board[i][j], end = " ")
# 		print()

# """ A recursive utility function to solve N
# Queen problem """
# def solveNQUtil(board, col):
    
# 	""" base case: If all queens are placed
# 		then return True """
# 	if (col >= N):
# 		return True
        
# 	""" Consider this column and try placing
# 		this queen in all rows one by one """
# 	for i in range(N):
        
# 		""" Check if the queen can be placed on board[i][col] """
# 		""" A check if a queen can be placed on board[row][col].
# 		We just need to check ld[row-col+n-1] and rd[row+coln]
# 		where ld and rd are for left and right diagonal respectively"""
# 		if ((ld[i - col + N - 1] != 1 and
# 			rd[i + col] != 1) and cl[i] != 1):
                
# 			""" Place this queen in board[i][col] """
# 			board[i][col] = 1
# 			ld[i - col + N - 1] = rd[i + col] = cl[i] = 1
            
# 			""" recur to place rest of the queens """
# 			if (solveNQUtil(board, col + 1)):
# 				return True
                
# 			""" If placing queen in board[i][col]
# 			doesn't lead to a solution,
# 			then remove queen from board[i][col] """
# 			board[i][col] = 0 # BACKTRACK
# 			ld[i - col + N - 1] = rd[i + col] = cl[i] = 0
            
# 			""" If the queen cannot be placed in
# 			any row in this column col then return False """
# 	return False
    
# """ This function solves the N Queen problem using
# Backtracking. It mainly uses solveNQUtil() to
# solve the problem. It returns False if queens
# cannot be placed, otherwise, return True and
# prints placement of queens in the form of 1s.
# Please note that there may be more than one
# solutions, this function prints one of the
# feasible solutions."""
# def solveNQ():
# 	board = [[0, 0, 0, 0],
# 			[0, 0, 0, 0],
# 			[0, 0, 0, 0],
# 			[0, 0, 0, 0]]
# 	if (solveNQUtil(board, 0) == False):
# 		printf("Solution does not exist")
# 		return False
# 	printSolution(board)
# 	return True
    
# # Driver Code
# solveNQ()

# # This code is contributed by SHUBHAMSINGH10

