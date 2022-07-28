import uuid
import sys

#TODO: 
# 1) cleanup and simplify the design in this code, 
#   a) place queens at locations by choice
#   b) move placed queens from location to location by choice (no restriction other than has piece or not)
#   c) logic for solutions of 8 queens game only, remove the regular chess elements like legal moves, etc.
# 2) introduce gui elements, 
# 3) introduce new functionality
#   a) Finding more solutions using alg1, specify how many, maybe randomize the seed and count the # of operations
#   b) Implement Backtracking algorithm, compare the efficiency of the two algorithms
#   c) Also create interactive way to cycle through solutions, maybe using a file to store them and implement a check solution button that verifies etc.
#   d) If possible create some kind of HINT feature that helps provide some AI to the program

# python 8 queens problem
DEBUG = False
CLI_MODE = True
MODE_GAME = 2

class Board():
    def __init__(self, grid_size):
        self.b_size = grid_size
        self.b_id = uuid.uuid1()
        self.b_solved = False
      
        #initial data structure 2d list, setup pieces and add_to_games()
        self.brd = [[None for i in range(grid_size)] for i in range(grid_size)]     
        self.add_to_games()
        self.make_chessboard()          
    
    def get_board(self):
        return self.brd

    def make_chessboard(self):
        for i in range(self.b_size):
            for j in range(self.b_size):
                self.brd[i][j] = (Square(self,i,j)) #create board with squares

    def add_to_games(self):
        games[self.b_id] =  self                    #map board to games

    def game_summary(self):
        return "".join(str(x) for x in move_history[self.b_id])

       
    @staticmethod
    def setup_queens(board):
        for i in board.brd:
            i[0].set_piece("Qu")
 
    @staticmethod
    def fetch_square(board,rank,file):
        return board[rank][file]
      
    def __repr__(self):
        return str(CLI_Output(self))

    # def board_solved(self):
        # algorithm_flag = 1
        # if algorithm_flag == 1:
            # self.board_solved_brute()
        # if algorithm_flag == 2:
            # self.board_solved_backtracking()


class Square():
    def __init__(self, board, file, rank):
        self.b_id = board.b_id
        self.piece = Piece(None,file,rank, self)
        self.location = (file,rank)                     #location[0], location[1]
        self.board = board.brd
        self.reset_square()                             #new squares piece type set to None

    def get_piece(self):
        return self.piece

    def get_piece_type(self):
        return self.piece.piece_type
        
    # def get_location(self):
        # return self.location

    def get_board_data(self):
        return self.board

    def get_board_id(self):
        return self.b_id

    def set_piece(self,type):
        self.piece = Piece(type,self.location[0],self.location[1],self)  #relies on garbage collection for old piece
        return 

    def has_piece(self):
        if self.piece.piece_type is None:
            return False
        return True

    def reset_square(self):
        self.set_piece(None)

    def __str__(self):
        if self.piece.piece_type is None:
            return ""
        return "%s%s" % (self.location[0], self.location[1]) + ":" + "%s\t" % (self.piece)

    def __repr__(self):
        return "Square" + str(self.get_piece())

class Piece():
    def __init__(self, type, file, rank, square):
        self.piece_type = type
        self.location = (file,rank)
        self.sqr = square
        self.b_id = square.b_id
        
    def get_square(self):
        brd = self.fetch_board(self).brd
        return brd[self.location[0]][self.location[1]]
    
    @staticmethod
    def fetch_board(piece):
        return games[piece.b_id]
        
    def move_to(self,x,y):
        b = self.fetch_board(self).brd
        sqr = Board.fetch_square(b,x,y)
        file = self.location[0]
        rank = self.location[1]
        move_history[self.b_id].append([self.piece_type,self.location,(x,y)])
        if not sqr.has_piece():
            old_square = b[file][rank]
            b[x][y].piece = self
            self.location = (x,y)
            old_square.reset_square()
            return self.location
        else:
            raise Exception("Illegal Move, piece already exists there.")
            return False  
        
    def __str__(self):
        if self.piece_type is None:
            return ""
        return str(self.piece_type) + '@' + ''.join(map(str,(chr(ord('A') + self.location[0]),self.location[1])))
        
        

class CLI_Output(Board):
    def __init__(self,boardgame):
        self.b_id = boardgame.b_id
        self.game = boardgame
        return None

    def __repr__(self):
        my_repr = ''
        if CLI_MODE:
            chess_repr = "Chessboard (CLI) Representation:\n"
            file = 'A'
            for i in range(self.game.b_size):
                rank = 1
                if i > 0:
                    chess_repr += "\n"
                    file = chr(ord(file) + 1)
                for j in range(self.game.b_size):
                    if j > 0:
                        rank += 1
                    chess_repr += file + str(rank) +':'+ str(self.game.brd[i][j])[-6:-4]+"\t"
            chess_repr += "\n"
            my_repr += chess_repr
        if DEBUG:
            data_repr = "Data Representation:\n"
            my_repr += data_repr + "".join(map(''.join,str(games[self.b_id].brd)))
        return my_repr


class Game():
    def __init__(self):
        global games
        games = {}

        global move_history
        move_history = {}
  
        self.b_game_mode = MODE_GAME    # 1,2  for auto/interactive

    @staticmethod
    def fetch_board(board):
        return games[board]

    @staticmethod
    def new_game(board):
        if DEBUG:
            print("newboard: " + str(board.b_id))
        games[board.b_id] = board
        move_history[board.b_id] = []


def main():
    g = Game()

#######     TESTING     ######################
# #game setup of Board.setup_queens        # #
##############################################

    #Create three new boards of different sizes
    g.new_game(Board(8))
    # g.new_game(Board(10))
    # g.new_game(Board(12))

    #Show the CLI output of squares with no pieces
    for uuid in games:
        print(g.fetch_board(uuid))

    #Call setup_queens() for each board
    for uuid in games:
        Board.setup_queens(g.fetch_board(uuid))
        print(g.fetch_board(uuid))

        

#######     TESTING     ######################
# #for Queen Gamepiece placement           # #
##############################################

    #Test of removal or addition of pieces  
    #N/A

    #Test of allowable moves
    for uuid in games:
        brd = g.fetch_board(uuid)
        sqr = brd.fetch_square(brd.brd,0,0)
    if sqr.has_piece():
        piece = sqr.get_piece()
        if brd.fetch_square(brd.brd,0,6).has_piece():
            raise Exception('not a legal move')
        else:
            piece.move_to(0,6)

    for board in games:
        print(g.fetch_board(board))
    
    
#######     TESTING     ######################
# # Input/Output               # #
##############################################

   #display the Move History 
    for board in games:
        print(g.fetch_board(board).game_summary())

    
#######     TESTING     ######################
# # Solutions Algorithms               # #
##############################################
    # for game in games:
        # if MODE_GAME == 1:
            # if DEBUG:
                # print("Solving...")
            # Solutions.solveNQ(games[uuid])
            # print(g)

        # elif MODE_GAME == 2:
            # Board.setup_queens(games[uuid])
      


        #Print the empty boards
        # print(g.fetch_board(uuid))
        #test move a piece
        # g.fetch_board(uuid).brd[0][0].move_piece(1,1)

        #Solve them
        # Solutions.solveNQ(g.fetch_board(uuid).brd)

main()

