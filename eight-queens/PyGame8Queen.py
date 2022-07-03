from qt import QtGui, QtWidgets, QtCore, _enum, _exec
import uuid
import Solutions

#TODO: 
# 1) cleanup and simplify the design in this code, 
# 2) introduce gui elements, 
# 3) introduce new functionality
#   a) Finding more solutions using alg1, specify how many, maybe randomize the seed and count the # of operations
#   b) Implement Backtracking algorithm, compare the efficiency of the two algorithms
#   c) Also create interactive way to cycle through solutions, maybe using a file to store them and implement a check solution button that verifies etc.
#   d) If possible create some kind of HINT feature that helps provide some AI to the program

# python 8 queens problem
DEBUG = True
MODE_GAME = 1

class Chesssquare():
    def __init__(self, board, file, rank):
        self.board = board
        self.location = (file,rank) #location[0], location[1]
        self.piece = Gamepiece(None,file,rank, board)
        self.reset_square()

    def get_board_id(self):
        return self.board.b_id

    def get_piece_type(self):
        return self.piece.piece_type

    def move_piece(self, x,y):
        if self.piece.islglmove(x,y):
            # save location for reset
            # old = self.get_square()
            move_history[self.get_board_id()].append([self.get_piece_type(),self.location,(x,y)])
            if self.get_board()[x][y].has_piece():
                #logic for capture made including points, and replacement(?)
                print("Capture")
                capture = games[self.b_id][x][y].piece
                move_history[-1].extend(['captures',str(capture)])
            self.get_board()[x][y].set_piece(self.get_piece_type())
            # self.piece_location = self.place_piece(x,y,self.piece_type)
            self.reset_square()
            # if self.get_square().location.board_solved():
            if DEBUG:
                print("debug - Move " + str(len(move_history[self.get_board_id()])) + ":" + str(move_history[self.get_board_id()][-1]))
            return True
        else:
            print("illegal move!")
        return False 

    def has_piece(self):
        if self.piece.piece_type is None:
            return False
        return True

    def set_piece(self,type):
        self.piece = Gamepiece(type,self.location[0],self.location[1],self.board)

    def get_piece(self):
        return self.piece

    def get_board(self):
        return self.board.brd

    def reset_square(self):
        self.set_piece(None)

    def __str__(self):
        if self.piece.piece_type is None:
            return "%s%s" % (self.location[0], self.location[1]) + ":  \t"
        return "%s%s" % (self.location[0], self.location[1]) + ":" + "%s\t" % (self.piece)

    def __repr__(self):
        return "Square" + str(self.get_piece())

class Game():
    def __init__(self):
        global games
        games = {}

        global move_history
        move_history = {}
        
    def new_game(self, board):
        if DEBUG:
            print("newboard: " + str(board.b_id))
        games[board.b_id] = board
        move_history[board.b_id] = []

    def fetch_board(self,uuid):
        return games[uuid]

class Board():
    def __init__(self, grid_size):
        self.b_id = uuid.uuid1()
        self.size = grid_size
        self.brd = self.board_structure(grid_size)

        #assigned to a global var
        games[self.b_id] =  self.brd
        self.make_chessboard()          #consider initial placement of pieces here

        # move_history[self.b_id] = []
        self.add_to_games()
    
    def get_board(self):
        return games[self.b_id]

    def add_to_games(self):
        games[self.b_id] =  self.brd    #games is global dictionary/map

    def make_chessboard(self):
        for i in range(self.size):
            for j in range(self.size):
                self.brd[i][j] = (Chesssquare(self,i,j))        # chessboard with chesssquares

    @staticmethod
    def board_structure(size):
        return [[None for i in range(size)] for i in range(size)]
        
    def get_board(self):
        return games[self.b_id]

    def game_summary(self):
        return "".join(str(x) for x in self.b_move_history)
        
    def __repr__(self):
        return str(CLI_Output(self))

class Queens(Board):
    def __init__(self, g_size):
        super().__init__(g_size)
        self.b_solved = False
        self.b_game_mode = MODE_GAME    # 1,2  for auto/interactive

        if MODE_GAME == 1:
            if DEBUG:
                print("Solving...")
            Solutions.solveNQ(games[self.b_id])
            print(self)

        elif MODE_GAME == 2:
            self.setup_queens(games[self.b_id])

    @staticmethod
    def setup_queens(board):
        for i in board:
            i[0].set_piece("Qu")
 
    def board_solved(self):
        algorithm_flag = 1
        if algorithm_flag == 1:
            self.board_solved_brute()
        if algorithm_flag == 2:
            self.board_solved_backtracking()
        
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
    
class CLI_Output(Board):
    def __init__(self,boardgame):
        self.b_id = boardgame.b_id
        self.game = boardgame
        return None

    def __repr__(self):
        my_repr = ''
        if True:
            chess_repr = "Chessboard (CLI) Representation:\n"
            file = 'A'
            for i in range(self.game.size):
                rank = 1
                if i > 0:
                    chess_repr += "\n"
                    file = chr(ord(file) + 1)
                for j in range(self.game.size):
                    if j > 0:
                        rank += 1
                    chess_repr += file + str(rank) +':'+ str(self.game.brd[i][j])[-3:-1]+"\t"
            chess_repr += "\n"
            my_repr += chess_repr
        if False:
            data_repr = "Data Representation:\n"
            my_repr += data_repr + "".join(map(''.join,str(games[self.b_id].brd)))
        return my_repr

class Gamepiece():
    def __init__(self, type, file, rank, board):
        self.b_id = board.b_id
        self.piece_type = type
        self.file = file
        self.rank = rank
        self.piece_location = board.brd[file][rank]
        if type is not None:
            # square = self.get_square(file,rank)
            self.place_piece(type)
    #         self.place_piece(file,rank,type)  #returns a file,rank tuple
        self.capture = False    #capture

    def fetch_piece(self):
        return games[self.b_id].brd[self.file][self.rank]

    def place_piece(self, type):
        self.piece_location.piece = self

    def get_square(self):
        return self.piece_location

    # def show_square(self):
    #     return str(self) + '@' + ''.join(map(str,self.piece_location))

    def islglmove(self,x,y):
        #logic for move by a queen along file or rank
        if self.file is x or self.rank is y:
            return True
        #logic for move by queen along diag
        elif abs(x - self.file) is abs(y - self.rank):
            return True
        else:
            return False

    def __str__(self):
        if self.piece_type is None:
            return ""
        return str(self.piece_type)


def main():
    g = Game()
    g.new_game(Queens(4))
    g.new_game(Queens(6))
    g.new_game(Queens(8))
    g.new_game(Queens(10))
    g.new_game(Queens(12))


    for uuid in games:
        #Print the empty boards
        # print(g.fetch_board(uuid))
        #test move a piece
        g.fetch_board(uuid).brd[0][0].move_piece(1,1)

        #Solve them
        # Solutions.solveNQ(g.fetch_board(uuid).brd)
        print(g.fetch_board(uuid))
# 

# #Unit Tests for Queen Gamepieces
#     q2 = Queen(0,1)
#     #test a move that is allowed
#     q2.move_piece(2,1)
#     print(b)

#     #test a move that is not allowed
#     q2.move_piece(0,2)    
#     print(b)

#     #test a move that is allowed
#     q2.move_piece(2,3)
#     print(b)

#     #test a move to where another piece is, i.e. takes piece
#     q2.move_piece(0,3)    
#     print(b)

    # print(b.game_summary())

    # user input/output for game start
    #choice = input()
    # board = new_game(game_type,game_difficulty_interactive)
    # b.place_queen(1,1)
    # b.place_queen(0,0)
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


