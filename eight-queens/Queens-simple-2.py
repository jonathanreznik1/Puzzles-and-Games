import uuid
import sys

# TODO:
# 1) Finish commenting and check file/rank row /col using paper-pencil
# 2) Add masking of paths to algorithm that solves
# 3) Add program graphics and interactive moves


# Flags
DEBUG = True
CLI_MODE = True
SOLVE = 1
           

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
        Game.games[board.id] = board        
   
    def __str__(self):
        """ String override method. Ret: String """
        my_str = ""
        # Loop through {} with keys and call __str__ method on each value
        for uuid in Game.games:
            my_str += self.fetch_board(uuid).__str__()
        return my_str        

class Square():
    """ Class for new squares """

    def __init__(self, board, rank, file):
        """ Constructor method for a square. Ret: None """
        self.b_id = board.id
        self.location = (rank, file)
        self.piece = None     # empty piece initially

    def set_queen(self):
        """ Assign a new piece object to square. None """
        self.piece = "Q"
       
    def has_piece(self):
        """ Checks for piece. Ret: Boolean """
        if self.piece is None:
            return False
        return True

    def reset(self):
        """ Removes object in square . Ret: None """
        self.piece = None
        
    def __str__(self):
        """ String override method. Ret: String """
        rank, file = self.location      # grab rank and file
        if not self.has_piece():
            # square is unoccupied by a piece
            return ""
        # square has piece output
        return "%s%s" % (rank, file) + ":" + "Qu\t"

    def __repr__(self):
        """ Representation override method. Ret: String """
        if self.has_piece():
            # unoccupied square
            return "Queen" + chr(ord("A")+self.location[1]) + "@" + str(self.location[1]) + str(self.location[0])
        return "Square@" + str(self.location[1]) + str(self.location[0])


class Board():
    """ Class for new boards """
    
    # new board gets assigned a uuid and dimension
    id = uuid.uuid1()
    solutions = {}              #to store solutions
        
    def __init__(self, dims):
        """ Constructor method for the board. Ret: None 
        Boards have a unique ID and dimension assigned there is also
        a fixed number of solutions that once found are entered into the
        class dictionary stored in class var "solutions"."""
        self.b_dims = dims
        self.b_solution_count = 0
        self.b_solved = False
        self.fresh_board()
        if DEBUG:
            print("new board: " + str(self.id))       
      

    def fresh_board(self):
        self.brd = [[Square(self,i,j) for i in range(self.b_dims)] for j in range(self.b_dims)]
        self.MOVES = 0
        if DEBUG:
            print("board cleared: " + str(self.id))
                
        
    @staticmethod
    def isSafe(brd, col, row):
        """ The method to check conflicts in squares. Ret: None """        
        # check within file for another piece
        for i in range(col):
#            print(row,i)
            sq = brd.brd[i][row]
            if sq.has_piece():
                return False
        # check along diag        
        for i, j in zip(range(row, -1, -1),
                        range(col, -1, -1)):
            print(j,i)
            sq = brd.brd[i][j]
            if sq.has_piece():
                return False
        # check along other diag
        for i, j in zip(range(row, len(brd.brd), 1),
                        range(col, -1, -1)):
            print(j,i)
            sq = brd.brd[i][j]
            if sq.has_piece():
                return False
        return True

    @staticmethod
    def Solve(board):
        """ Static method to solve a board. Ret: Boolean """    
        global SOLVE
        i = 0
        
        while i < SOLVE:
            if Board.SolveRemaining(board, 0) == False:
                print("No solution")
                return False
            
            Board.solved(i,board)
            
            board.fresh_board()
            board.reset_move_count()
            i+=1
        # return board.b_solved  
        
        return board.solutions      

    @staticmethod
    def SolveRemaining(board,col):
        """ Recursive method for solving the n queens board. Ret: Boolean """  
        #global MOVES
        if col >= board.b_dims:
            if Board.visited(board):
                return False
            return True
        
        for row in range(board.b_dims):
            # Board.add_move(board)
            if Board.isSafe(board, col, row):
                square = board.brd[row][col]
                square.set_queen()
                # while SOLVE_COUNT < 10:
                    # if board.found_already():
                        #  print("hello")
                        #  continue
                if Board.SolveRemaining(board, col + 1) == True:
                    return True
                square.reset()
        return False

    def solved(sol,brd):
        print("Solved another board")
            #register the board solution using a better method
        Board.solutions[sol]=brd.get_solution()
        print(Board.solutions[sol])


    @staticmethod
    def matches(board1,board2):
        """ Board 2 is an existing board and Board 1 is the new board """
        comp = Board.get_solution(board1)
        for [i,j] in comp:
            if [i,j] not in board2:
                return False
        return True

    @staticmethod
    def visited(board):
        if len(board.solutions)==0:
            return False
        for solved in board.solutions.values():
            if Board.matches(board,solved) == True:
                return True
        return False

    def get_solution(board):
        s = []
        for j in range(board.b_dims):
            for i in range(board.b_dims):
                if board.brd[i][j].has_piece():
                    s.append([i,j])
        return s

    def reset_move_count(board):
        board.MOVES = 0

    def add_move(board):
        board.MOVES += 1

    def __repr__(self):
        """ Representation override method. Ret: String """
        my_repr = ''
        # if self.b_solved:
        if self.b_solved:
            my_repr += "Board Solved in %i moves!\n" % (self.MOVES)
        if CLI_MODE:
            my_repr += CLI.ShowBoard(self)
        if DEBUG:
            my_repr += "Data Representation:\n" + "".join(map(''.join,str(
                Game.games[self.id].brd))) + "\n"
        return my_repr


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

    def ShowSolution(solution):
        chess_repr = "Chessboard (CLI Mode):\n"
        b_dims = len(solution)
        rank = b_dims
        for i in range(b_dims):
            file = 'A'
            if i > 0:
                rank -= 1
                chess_repr += "\n"
            for j in range(b_dims):
                if j > 0:
                    file = chr(ord(file)+1)
                chess_repr += file + str(rank) +':'
                if [i,j] in solution:
                    chess_repr += 'Qu'
                chess_repr += "\t"
        chess_repr += "\n"
        return chess_repr


def main():

    # new game
    g = Game()
   
    # three new boards
    b1 = Board(8)
    #b2 = Board(8)
    #b3 = Board(9)
    g.new_game(b1)
    #g.new_game(b2)
    #g.new_game(b3)
    
    # print(g)
   
    # solve each of the boards
    for uuid in g.games:
        b = g.fetch_board(uuid)
        Board.Solve(b)
        print(Board.solutions)
        for solution in Board.solutions.values():
            # print(len(solution))
            print(CLI.ShowSolution(solution))


    #     print(b)


main()

