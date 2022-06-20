from PyQt6.QtWidgets import *

#New python project 8 queens problem

# 1. Data structures board - positional elements
# class boardgame():

class board():
    global board
    def __init__(self, grid_size):
        self.grid_size = grid_size
    

class game(board):
    def __init__(self, size, type):
        super().__init__(size)
        self.game = type
        self.board = self.board_structure(size)

    def board_structure(self,gridsize):
        self.board = []
        for i in range(gridsize):
            self.board.append([])

class chessboardsquare():
    def __init__(self, rank, file):
        

    # TODO: need to work on this function
    def board_positions(self):
        return self.board

    # TODO: need to work on this function for algorithm for checking solution goes here
    def board_solved(self):
        # separate functional solutions for different algorithms such as backtracking and brute force
        return True
    
    # def board_Nqueens(self,n):
    #     self.board_structure(n)

    #     result = []
    #     #with alphabet list
    #     start = ord('A')
    #     files = []
    #     for i in range(grid):
    #         files.append(chr(start + i))
    #     for file in files:
    #         result.append([])
    #         for ranks in range(grid):
    #             val = file + str(ranks+1)
    #             result[ord(file)-ord('A')].append(val)
    #     return result
    
    # def new_board_game(board):
    #     dict

    def __str__(self):
        # mystring=' '.join(map(str,self.board))
        # return mystring
        return "%s" % (self.board)

    def __rep__(self):
        mystring=' '.join(map(str,self.board))
        return mystring



class boardpiece():
    global piece
    def __init__(self, piece_type):
        self.piece_type = piece_type
    
    def place_piece(self, file, rank):
        board[file][rank] = self

    def __str__(self):
        return "piece"


# class queen(boardpiece):
#     def __init__(self, piece_type):
#         super().__init__(piece_type)

#     def place_queen(self,file,rank):
#         self.board[file][rank] = 'q'


# def printSolution(board):
#     for i in range(N):
#         for j in range(N):
#             print(board[i][j], end = " ")
#         print()

    # define options for entering queen position by rank/file, rank or file
    # input/output with error handling

def main():
    b = Ngame(4,"queens")
    # user input/output for game start
    #choice = input()
    # board = new_game(game_type,game_difficulty_interactive)
    # b.place_queen(1,1)
    # b.place_queen(0,0)
    print(b)

main()
#  b. pieces - object

# 2. Functions 
#  a.  the rules of the game
#  b.  helping functions (New board / Losing board / Winning board)
#  c.  undo -  optional if it is not a lot of extra programming
# 3. Graphics
#  a. qt for ctype python rendering
#  b. board empty
#  c. redrawing the board with pieces
# 4. Main program (menu)
#  a. Manual
#  b. Automatic
#  c. Run gaming loop with while(true) statement


