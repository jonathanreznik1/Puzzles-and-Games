from qt import QtGui, QtWidgets, QtCore, _enum, _exec

# python 8 queens problem

class Board():
    def __init__(self, grid_size):
        global board
        board = self.board_structure(grid_size)
        self.grid_size = grid_size

    def board_structure(self,size):
        brd = []
        file = 'A'
        for i in range(size):
            brd.append([])
            rank = 1
            if i > 0:
                file = chr(ord(file) + 1)
            for j in range(size):
                if j > 0:
                    rank += 1
                brd[i].append(Chesssquare(file,str(rank)))
        return brd

    # TODO: need to work on this function for algorithm for checking solution goes here
    # separate functional solutions for different algorithms such as backtracking and brute force
    def board_solved(self):
        return True
    
    def __repr__(self):
        return "this is __repr__"

class Chesssquare():
    def __init__(self, file, rank):
        self.file = file
        self.rank = rank
        self.piece = None

    def __str__(self):
        if self.piece is not None:
            return "%s\t" % (self.piece)
        else:
            return "%s%s\t" % (self.file, self.rank)

    # def __str__(self,debug):
    #     return "%s%s-%s" % (self.file, self.rank, self.piece)
    

class Gamepiece():
    def __init__(self, type, file, rank):
        self.piece_type = type
        self.piece_location = self.place_piece(file, rank)
    
    def place_piece(self, file, rank):
        board[file][rank].piece = self
        return file,rank

    def at_square(self):
        return ''.join(map(str,self.piece_location))

    def __str__(self):
        return self.piece_type

class Queen(Gamepiece):
    def __init__(self,f,r):
        super().__init__("Qu",f,r)
    
    # def move_piece():

    # def lglmove():


class Game(Board):
    def __init__(self, size, type):
        super().__init__(size)
        self.game = type
        board = self.board_structure(size)

    def __repr__(self):
        my_board_repr = ""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                 my_board_repr += str(board[i][j])
                #  "this is __repr__"
        return my_board_repr

def main():
    b = Game(4,"queens")
    p1 = Queen(0,0)
    p2 = Queen(2,3)

    # user input/output for game start
    #choice = input()
    # board = new_game(game_type,game_difficulty_interactive)
    # b.place_queen(1,1)
    # b.place_queen(0,0)
    print(b)
    print(p1.at_square())
    print(p2.at_square())
    # print(b.board)
    # print(b.board[0])

main()

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


