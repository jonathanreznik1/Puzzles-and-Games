from PyQt6.QtWidgets import *

#New python project 8 queens problem

# 1. Data structures board - positional elements
class boardgame():
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.board = self.new_board_structure(grid_size)

    def new_board_structure(self,grid_size):
        board = []
        #with alphabet list
        alpha = ['a','b','c','d','e','f','g','h']
        #with byte string
        # ch = bytes('A', 'utf-8')
        for files in range(grid_size):
            # ch = bytes(ch[0]+1)
            board.append([])
            for ranks in range(grid_size):
                val = alpha[files] + str(ranks+1)
                # val = str(ch.decode("utf-8")) + str('M')
                board[files].append(val)
        return board

    def place_queen(self,file,rank):
        self.board[file][rank] = 'q'

    def __str__(self):
        mystring=' '.join(map(str,self.board))
        return mystring

# def check_board():

def winning_board():
    # recursive or iterative solution

def new_game():
    global b
    b = boardgame(8)
    
    #gather some basic information about the user such as name and skill leve, etc.
    username = input("Name:")
    difficulty = input("Difficulty (easy, medium, difficult)") 

board = new_game()
b.place_queen(1,1)
print(b)
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


