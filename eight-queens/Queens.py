import uuid
import sys

# TODO:
# 1) Finish commenting
# 2) Add masking of paths
# 3) Count moves made and show
# 4) Alternate solutions mathematically


# Flags
DEBUG = False
CLI_MODE = True
SOLVE_COUNT = 10

class Piece():
    """ Class for new pieces """

    def __init__(self, p, square, board):
        """ Constructor method for class. Ret: None """
        self.b_id = board.b_id
        self.p_location = square.location
        self.p_type = p
    
    def fetch_square(self):
        """ The static method to fetch square from a board. Ret: Square """
        brd = Game.fetch_board(self.b_id)
        rank, file = self.p_location
        return brd[rank][file]

    def __str__(self):
        """ String override method. Ret: String """
        if self.p_type == "Q":
            # show piece
            return "Qu"
        elif self.p_type == None:
            # if no piece exists show str for square object
            return Piece.fetch_square(self)
           
           
class Square():
    """ Class for new squares """

    def __init__(self, board, rank, file):
        """ Constructor method for a square. Ret: None """
        self.b_id = board.b_id
        self.location = (rank, file)
        self.piece = Piece(None,self,board)     # empty piece initially

    def set_piece(self, piece):
        """ Assign a new piece object to square. None """
        self.piece = piece
       
    def has_piece(self):
        """ Checks for piece. Ret: Boolean """
        if self.piece.p_type is None:
            return False
        return True

    def reset_square(self):
        """ Removes and places new piece object in square . Ret: None """
        B = Game.fetch_board(self.b_id)     # grab the board
        self.set_piece(Piece(None,self,B))
        
    def __str__(self):
        """ String override method. Ret: String """
        rank, file = self.location      # grab rank and file
        if not self.has_piece():
            # square is unoccupied by a piece
            return ""
        # square has piece output
        return "%s%s" % (file, rank) + ":" + "%s\t" % (self.piece)

    def __repr__(self):
        """ Representation override method. Ret: String """
        if self.has_piece():
            # unoccupied square
            return "Queen" + chr(ord("A")+self.location[1]) + "@" + str(self.location[1]) + str(self.location[0])
            return self.piece.p_type
        # occupied square
        return "Square@" + str(self.location[1]) + str(self.location[0])


class Game():
    """ Class with a dictionary and static methods to create board games """
    games = dict()
    
    @staticmethod
    def fetch_board(uuid):
        """ The static method to fetch a board based on board id Ret: Board """
        return Game.games[uuid]     # calls class variable games which is {}

    @staticmethod
    def new_game(board):        
        """ The static method to add a new board to games Ret: None"""
        # The games {} gets a new entry with key: uuid and value: Board object
        Game.games[board.b_id] = board        
   
    def __str__(self):
        """ String override method. Ret: String """
        my_str = ""
        # Loop through {} with keys and call __str__ method on each value
        for uuid in Game.games:
            my_str += self.fetch_board(uuid).__str__()
        return my_str        


class Board():
    """ Class for new boards """

    b_dims = 8
    b_id = uuid.uuid1()
        
    def __init__(self, dims):
        """ Constructor method for the board. Ret: None """
        # new board gets assigned a uuid and dimension
        # self.b_solved = False
        self.MOVES = 0
        self.solutions = []
        self.brd = [[Square(self,i,j) for j in range(Board.b_dims)] for i in range(Board.b_dims)]               
        # self.reset_board(self)
        if DEBUG:
            print("newboard: " + str(Board.b_id))       
        
    @staticmethod    # data structure
    def reset_board(board):
        board.brd = [[Square(board,i,j) for j in range(Board.b_dims)] for i in range(Board.b_dims)]
        

    def __repr__(self):
        """ Representation override method. Ret: String """
        my_repr = ''
        # if self.b_solved:
        if self.solutions:
            my_repr += "Board Solved in %i moves!\n" % (self.MOVES)
        if CLI_MODE:
            my_repr += CLI.ShowBoard(self)
        if DEBUG:
            my_repr += "Data Representation:\n" + "".join(map(''.join,str(
                Game.games[Board.b_id].brd))) + "\n"
        return my_repr

    def add_solution(board):
        s = []
        for j in range(Board.b_dims):
            for i in range(Board.b_dims):
                if board.brd[i][j].has_piece():
                    s.append([i,j])
        board.solutions.append(s)

    def reset_move_count(board):
        board.MOVES = 0

    @staticmethod
    def Solve(board):
        """ Static method to solve a board. Ret: Boolean """    
        global SOLVE_COUNT
        while SOLVE_COUNT > 0:
            if Board.SolveRemaining(board, 0) == False:
                print("No solution")
                return False
            # board.b_solved = True
            print(board)
            SOLVE_COUNT -= 1
            #register the board solution using a better method
            board.add_solution()
            board.reset_board(board)
            board.reset_move_count()
            # return board.b_solved  
        return board.solutions      

    def add_move(board):
        board.MOVES += 1

    @staticmethod
    def SolveRemaining(board,col):
        """ Recursive method for solving the n queens board. Ret: Boolean """  
        #global MOVES
        if col >= board.b_dims:
            return True
        
        for row in range(board.b_dims):
            Board.add_move(board)
            if Board.isSafe(board.brd, row, col):
                sq = board.brd[row][col]
                q = Piece("Q",sq,board)
                sq.set_piece(q)
                while SOLVE_COUNT < 10:
                    if board.found_already():
                        #  print("hello")
                         continue
                if Board.SolveRemaining(board, col + 1) == True:
                    return True
                sq.reset_square()
        return False

    def found_already(board):
        if board.solutions is False:
            return
        for solved in board.solutions:
            return board.match_boards(board,solved)

    @staticmethod
    def match_boards(board1,board2):
        for i in range(Board.b_dims):
            for j in range(Board.b_dims):
                if board1.brd[i][j].has_piece():
                    if [i,j] not in board2:
                        return False
        return True

    @staticmethod
    def isSafe(brd, row, col):
        """ Constructor method for the square. Ret: None """

        # 
        for i in range(col):
            if brd[row][i].has_piece():
                return False

        # 
        for i, j in zip(range(row, -1, -1),
                        range(col, -1, -1)):
            if brd[i][j].has_piece():
                return False

        # 
        for i, j in zip(range(row, len(brd), 1),
                        range(col, -1, -1)):
            if brd[i][j].has_piece():
                return False
        return True


class CLI():
    """ Class of static methods for transforming boards to pretty CLI output"""

    @staticmethod
    def ShowBoard(board):
        """ Static method to print boards and pieces to cli. Ret: String """
        chess_repr = "Chessboard (CLI Mode):\n"
        b_dims = board.b_dims                 #TODO: Fix if isn't square
        rank = b_dims
        for i in range(b_dims):
            file = 'A'
            if i > 0:
                rank -= 1
                chess_repr += "\n"
            for j in range(b_dims):
                if j > 0:
                    file = chr(ord(file) + 1)
                chess_repr += file + str(rank) +':'+ str(board.brd[i][j])[-3:
                    -1]+"\t"
        chess_repr += "\n"  
        return chess_repr


def main():

    # new game
    g = Game()
   
    # three new boards
    b1 = Board(6)
    # b2 = Board(10)
    # b3 = Board(12)
    g.new_game(b1)
    # g.new_game(b2)
    # g.new_game(b3)
    
    print(g)
   
    # solve each of the boards
    for uuid in g.games:
        b = g.fetch_board(uuid)
        Board.Solve(b)

    print(g)

    # for b in b1.solutions:
    #     print(b)


main()

