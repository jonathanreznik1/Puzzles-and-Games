import uuid
import sys

#TODO: 
# 1) cleanup and simplify design 
# 2) introduce gui elements 
# 3) Solutions file for single board
#   Implement Backtracking algorithm, compare the efficiency of the two algorithms
# 4) Expand on solutions introducing concurrency
#   Interactive cycling through the solutions, maybe using a file to store or check solutions
# 5) Create HINT feature with some AI or greedy algorithm

# python 8 queens problem
DEBUG = True
MOVE_DEBUG = True
CLI_MODE = False
MODE_GAME = 2


class Piece():
#A piece is placed on a square at a specific file and rank
    def __init__(self, piece_type, file, rank, board):
        self.b_id = board.b_id
        self.p_location = (file,rank)
        self.p_type = piece_type
    
    def fetch_board(self):
        return games[self.b_id]

    # def fetch_square(self):
        # file = self.location[0]
        # rank = self.location[1]
        # return games[self.b_id].brd[rank][file]            
        
    def move_queen(self,square):
    #Move piece from current location to x,y
        file = self.p_location[0]
        rank = self.p_location[1]
        
        board = self.fetch_board()
        b = board.brd                     #brd is a 2d list structure
        x,y = square.get_location()
        sqr = Board.fetch_square(b,x,y)
        
        if not sqr.has_piece():
            move_history[self.b_id].append([self.p_type,self.p_location,(x,y)])
            old_square = b[file][rank]
            b[x][y].piece = self
            self.p_location = (x,y)
            old_square.reset_square()
            return self.p_location
        else:
            raise Exception("Illegal Move, piece already exists there.")
            return False  
        
    def __str__(self):
        if self.p_type is "QUEEN":
            return "Qu"
        # return self.p_type + '@' + ''.join(map(str,(chr(ord('A') + self.location[0]),self.fetch_board(self).b_size - self.location[1])))
        

class Square():
    def __init__(self, board, rank, file):
        self.b_id = board.b_id
        self.piece = Piece(None,file,rank,board)
        self.location = (rank, file)                     #rank location[0], file location[1]
        self.board = board.brd
        self.reset_square()                             #new squares piece type set to None

    def get_piece(self):
        return self.piece
       
    def get_location(self):
        return self.location[0],self.location[1]
        
       
    def get_rank(self):
    #actual rank counts down from b_size to 1
        return self.get_board_size() - self.location[0]

    def get_file(self):
        return chr(ord('A')+self.location[1])

    def fetch_board(self):
        return games[self.b_id]
        
    def get_board_data(self):
        return self.board

    def get_board_id(self):
        return self.b_id
        
    def get_board_size(self):
        board = self.fetch_board()
        return board.b_size

    def set_piece(self,p_type):
        self.piece = Piece(p_type,self.location[1],self.location[0],self.fetch_board())  #relies on garbage collection for old piece
        return 

    def has_piece(self):
        if self.piece.p_type is None:
            return False
        return True

    def reset_square(self):
        self.set_piece(None)

    def __str__(self):
        if self.piece.p_type is None:
            return ""
        return "%s%s" % (self.location[1], self.location[0]) + ":" + "%s\t" % (self.piece)

    def __repr__(self):
        if self.has_piece():
            return self.piece.p_type
        return "Square"
        
class Board():
    def __init__(self, grid_size):
        self.b_size = grid_size
        self.b_id = uuid.uuid1()
        self.brd = [[None for i in range(grid_size)] for i in range(grid_size)]     
        self.add_to_games()
        self.make_chessboard()          
        self.b_solved = False
    
    def make_chessboard(self):
        #i is the complement of rank and j is the complement of file for boardsize
        for i in range(self.b_size):
            for j in range(self.b_size):
                self.brd[i][j] = (Square(self,i,j)) #create board with squaress

    def add_to_games(self):
        games[self.b_id] =  self                    #map board to games

    # def game_summary(self):
        # return 

    def get_board(self):
        return self.brd
       
    @staticmethod
    def fetch_square(board,rank,file):
        return board[rank][file]
      
    @staticmethod
    def setup_queens(board):
        for i in board.brd:
            i[0].set_piece("QUEEN")
 
    def __repr__(self):
        my_repr = ''
        chess_repr = "Chessboard (CLI) Representation:\n"
        if self.b_solved:
            chess_repr += "Board Solved!\n"
        dim = self.b_size
        rank = dim
        for i in range(dim):
            file = 'A'
            if i > 0:
                rank -= 1
                chess_repr += "\n"
            for j in range(dim):
                if j > 0:
                    file = chr(ord(file) + 1)
                chess_repr += file + str(rank) +':'+ str(self.brd[i][j])[-3:-1]+"\t"
        chess_repr += "\n"
        my_repr += chess_repr
        if DEBUG:
            my_repr += "Data Representation:\n" + "".join(map(''.join,str(games[self.b_id].brd))) + "\n"
        if MOVE_DEBUG:
            my_repr += "Game Representation:\n" + "".join(str(x) for x in move_history[self.b_id])
        return my_repr


    # def board_solved(self):
        # algorithm_flag = 1
        # if algorithm_flag == 1:
            # self.board_solved_brute()
        # if algorithm_flag == 2:
            # self.board_solved_backtracking()
            


        
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
    g.new_game(Board(10))
    # g.new_game(Board(12))

    #Show the CLI output of squares with no pieces
    for uuid in games:
        print(g.fetch_board(uuid))

    #Call setup_queens()
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
                piece.move_queen(brd.fetch_square(brd.brd,0,6))

    for board in games:
        print(g.fetch_board(board))
    
    
#######     TESTING     ######################
# # Input/Output               # #
##############################################

   #display the Move History 
    # for board in games:
        # print(g.fetch_board(board).game_summary())

    
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

