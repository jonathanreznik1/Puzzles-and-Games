import Solutions
import uuid
import sys

# python 8 queens

DEBUG = True
CLI_MODE = True
GAME_MODE = 1     #1)Solve or 2)Check

class Square():

    def __init__(self, board, rank, file):
        """ Constructor method for the square. Ret: None """
        self.b_id = board.b_id
        self.location = (rank, file)                     #rank location[0], file location[1]
        self.piece = Piece(None,self,board)

    def has_piece(self):
        """ Checks for piece. Ret: Boolean """
        if self.piece.p_type is None:
            return False
        return True

    def set_piece(self, piece):
        """ Assign piece to a square. None """
        self.piece = piece

    def reset_square(self):
        """ Removes piece from square . Ret: None """
        rank,file = self.location
        B = Game.fetch_board(self.b_id)
        self.piece = Piece(None,self,B)
        
    def get_piece(self):
        """ Getter for piece attribute. Ret: Piece """
        return self.piece
       
    def __str__(self):
        """ String override method. Ret: String """
        rank, file = self.location
        # print(rank,file)
        if not self.has_piece():
            return ""
        return "%s%s" % (file, rank) + ":" + "%s\t" % (self.piece)

    def __repr__(self):
        """ Representation override method. Ret: String """
        if self.has_piece():
            return self.piece.p_type
        return "Square"

class Piece():

    # def __init__(self, pie, file, rank, board):
    def __init__(self, pie, square, board):
        """ Constructor method for class. Ret: None """
        self.b_id = board.b_id
        rank = square.location[0]
        file = square.location[1]
        self.p_location = (file,rank)
        self.p_type = pie
    
    def __str__(self):
        """ String override method. Ret: String """
        if self.p_type == "Qu":
            return "Qu"
                
class Board():

    def __init__(self, dims):
        """ Constructor method for the board. Ret: None """
        self.b_id = uuid.uuid1()        #assigns a unique id
        self.brd = [[Square(self,i,j) for j in range(dims)] for i in range(dims)]               
        self.b_dim = dims
        self.b_solved = False
        if DEBUG:
            print("newboard: " + str(self.b_id))       
        
    def __repr__(self):
        """ Representation override method. Ret: String """
        my_repr = ''
        if self.b_solved:
            my_repr += "Board Solved!\n"
        if CLI_MODE:
            my_repr += CLI.ShowBoard(self)
        my_repr += "Data Representation:\n" + "".join(map(''.join,str(Game.games[self.b_id].brd))) + "\n"
        return my_repr

class Game():
    games = dict()
    
    @staticmethod
    def fetch_board(uuid):
        """ The static method to fetch a board based on board id Ret: Board """
        return Game.games[uuid] 

    @staticmethod
    def fetch_square(board,rank,file):
        """ The static method to fetch square from a board. Ret: Square """
        return board[rank][file]

    @staticmethod
    def setup_queens(board):
        """ The static method places Pieces diagonal of squares Ret: None"""
        for i,item in enumerate(board.brd):
            sqr = board.brd[i][i]
            item[i].piece = Piece("Qu",sqr,board)

    @staticmethod
    def new_game(board):        
        Game.games[board.b_id] = board           #map board to games
        
   
    def __str__(self):
        my_str = ""
        for uuid in Game.games:
            my_str += self.fetch_board(uuid).__str__()
        return my_str


class CLI():

    @staticmethod
    def ShowBoard(board):
        chess_repr = "Chessboard (CLI Mode):\n"
        b_dim = board.b_dim                 #TODO: Fix if isn't square
        rank = b_dim
        for i in range(b_dim):
            file = 'A'
            if i > 0:
                rank -= 1
                chess_repr += "\n"
            for j in range(b_dim):
                if j > 0:
                    file = chr(ord(file) + 1)
                chess_repr += file + str(rank) +':'+ str(board.brd[i][j])[-3:-1]+"\t"
        chess_repr += "\n"
        return chess_repr


def main():
    g = Game()

    #Tests 
    #   Index 0: game setup 
    #   Index 1: 
    #   Index n: multiple boards solved sequentially with backtracking algorithm
    TestSuite = [1,1,1,1]
    
#######     TESTING     ######################
## game setup of Board.setup_queens         ##
##############################################
    if TestSuite[0]:    
    ## Board()
    ## new_game()
    
    
    ##Create three new boards and add them to games
        b1 = Board(8)
        g.new_game(b1)

        b2 = Board(7)
        g.new_game(b2)

        b3 = Board(6)
        g.new_game(b3)

        ###Board output
        #print(g)
   

#######     TESTING     ######################
## Square method testing                    ##
##############################################
            
    if TestSuite[1]:
        UnitTest = [1,1,1,1,0]
        
        if UnitTest[0]:
        ## get_piece()
            print("Checkin square method to query pieces...",end="")
            for col in b1.brd:
                for square in col:

                    assert isinstance(square.get_piece(),Piece), "Not pieces"

            print("pass")

            ##Board output
            print(g)
        
        if UnitTest[1]:
        ## set_piece()
            print("Checkin square method for setting new pieces...",end="")
            for col in b1.brd:
                for square in col:

                    square.set_piece(Piece("Qu",square,b1))

                    assert square.get_piece().p_type=="Qu", "Not queen"

            print("pass")
        
            ##Board output
            print(g)
        
        if UnitTest[2]:
        ## has_piece()
            print("Checking number of pieces: ",end="")
            count = 0
            for i,col in enumerate(b1.brd):
                for square in b1.brd[i]:
                   if square.has_piece():
                        count += 1
            print(count)
            
            ##Board output
            print(g)
        

    ## reset_piece()

        

        

        ##reset_piece()
        for uuid in g.games:
            b = g.fetch_board(uuid)
            #remove all queens
            for rank in range(b.b_dim):
                for file in range(len(b.brd[rank])):
                    b.brd[rank][file].reset_square()
        print(g)

    
#######     TESTING     ###############
##    Gamepiece placement           # #
#######################################

    if TestSuite[2]:
        pass
   
#######     TESTING     ######################
## Solutions Algorithms               # #
##############################################

    if TestSuite[3]:
    # Setup the tests for solving N-queens with brute force
        for uuid in g.games:
            b = g.fetch_board(uuid)
            g.setup_queens(b)
    
    # 
            
    # Solve N-queens problem with brute force algorithm
        # for uuid in g.games:
            # b = g.fetch_board(uuid)
            # print("Solving...")
            # Solutions.board_solve(2,b.brd)
    
        print(g)

    # #Solve N-queens problem with Recursive Solution
        # for uuid in g.games:
            # if DEBUG:
                # print("Solving...")
            # Solutions.solveNQ(g.fetch_board(uuid).brd)
    # print(g)

main()

