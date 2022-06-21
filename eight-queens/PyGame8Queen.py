from qt import QtGui, QtWidgets, QtCore, _enum, _exec

# python 8 queens problem

class Board():
    def __init__(self, grid_size, game_type):
        global grid
        grid = grid_size
        self.game = game_type
        global board
        board = self.board_structure(grid_size)

    def board_structure(self,size):
        brd = []
        for i in range(size):
            brd.append([])
            for j in range(size):
                brd[i].append(None)
        return brd

    @staticmethod
    def make_chess_board():
        for i in range(grid):
            for j in range(grid):
                board[i][j] = (Chesssquare(i,j))

    # def board_structure(self,size):
    #     brd = []
    #     file = 'A'
    #     for i in range(size):
    #         brd.append([])
    #         rank = 1
    #         if i > 0:
    #             file = chr(ord(file) + 1)
    #         for j in range(size):
    #             if j > 0:
    #                 rank += 1
    #             brd[i].append(Chesssquare(file,str(rank)))
    #     return brd

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
        self.piece = Gamepiece(None,file,rank)

    def __str__(self):
        return "%s%s" % (self.file, self.rank) + ":" + "%s\t" % (self.piece)

    # def __str__(self,debug):
    #     return "%s%s-%s" % (self.file, self.rank, self.piece)


class Gamepiece():
    def __init__(self, type, file, rank):
        self.piece_type = type
        self.piece_location = (file,rank)
        # self.place_piece(file, rank)

#        return file,rank
    def place_piece(self, file, rank, type):
        board[file][rank].piece = Gamepiece(type,file,rank)
        self.piece_location = (file,rank)

    def reset_piece(self):
        file = self.piece_location[0]
        rank = self.piece_location[1]
        board[file][rank].piece.piece_type = None

    def show_square(self):
        return str(self) + '@' + ''.join(map(str,self.piece_location))

    def move_piece(self, x,y):
        if self.islglmove(x,y):
            temp = self
            self.reset_piece()
            self.place_piece(x,y,temp.piece_type)

    def __str__(self):
        if self.piece_type is None:
            return "N"
        return self.piece_type

class Queen(Gamepiece):
    def __init__(self,f,r):
        super().__init__("Qu",f,r)
        self.place_piece(f,r,"Qu")
    
    def islglmove(self,x,y):
        if self.piece_location[0] is x or self.piece_location[1] is y:
            return True
        elif x - self.piece_location[0] is y - self.piece_location[1]:
            return True
        else:
            return False

class Game(Board):
    def __init__(self, g_size, g_type):
        super().__init__(g_size,g_type)
        if g_type == "queens": 
            board = self.make_chess_board()

    def __repr__(self):
        my_board_repr = "Board:\n"
        for i in range(grid):
            for j in range(grid):
                my_board_repr += str(board[i][j])
                if j is (grid - 1):
                    my_board_repr += "\n"
                #  "this is __repr__"
        return my_board_repr

def main():
    b = Game(4,"queens")
    q1 = Queen(2,0)
    q2 = Queen(0,1)
    q3 = Queen(3,2)
    q4 = Queen(1,3)
    q2.move_piece(2,1)
    q2.move_piece(0,1)    
    # user input/output for game start
    #choice = input()
    # board = new_game(game_type,game_difficulty_interactive)
    # b.place_queen(1,1)
    # b.place_queen(0,0)
    print(b)
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


