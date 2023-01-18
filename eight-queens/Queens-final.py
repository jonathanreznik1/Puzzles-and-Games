import uuid
import sys


'''
This program will be able to solve an N queens problem using a backtracking
algorithm that is basically somewhat brute force.  There is no solution masking
in the algorithm.  It is capable of calculating up to 19 queens in a reasonable
length of time, and then it becomes unmanageable haha.
'''


# Flags
DEBUG = True
CLI_MODE = True

# Other Input
BOARDS = (8,)  # enter a tuple here of the boards to solve
# NOTE: The order of solutions found will be the same each time so rather than
# include the same number twice (for now!) use the next param to alter the
# number of solutions attempted.
SOLVE = (93,)  # enter the max number of solutions to find in each board

# TODO:
# Add masking paths in algorithm and other efficiencies
# Create more interactive user input/output


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

    # def __str__(self):
    #     """ String override method. Ret: String """
    #     rank, file = self.location      # grab rank and file
    #     if not self.has_piece():
    #         return ""
    #     return "Qu"

    def __repr__(self):
        """ Representation override method. Ret: String """
        rank, file = self.location
        if self.has_piece():
            # unoccupied square
            return "QU@" + chr(ord("A")+file) + str(rank+1)
        return "sq@" + chr(ord("A")+file) + str(rank+1)


class Board():
    """ Class for new boards """

    # new board gets assigned a uuid and dimension
    solutions = {}  # to store solutions

    def __init__(self, dims):
        """ Constructor method for the board. Ret: None 
        Boards have a unique ID and dimension assigned
        There is a fixed number of solutions to each one.
        Once found entered into "solutions" map."""
        self.id = uuid.uuid1()
        self.b_dims = dims
        self.b_index = BOARDS.index(dims)

        self.b_solution_count = 0

        self.fresh_board()
        if DEBUG:
            print("new board: " + str(self.id))

    def fresh_board(self):
        self.brd = [[Square(self, i, j) for i in range(self.b_dims)]
                    for j in range(self.b_dims)]
        self.MOVES = 0
        self.b_solved = False
        if DEBUG:
            print("board cleared: " + str(self.id))

    @staticmethod
    def isSafe(brd, row, col):
        """ The method to check conflicts in squares. Ret: None """
        # check within file for another piece
        for i in range(col):
            #            print(row,i)
            sq = brd.brd[row][i]
            if sq.has_piece():
                return False
        # check along diag
        for i, j in zip(range(row, -1, -1),
                        range(col, -1, -1)):
            #            print(j,i)
            sq = brd.brd[i][j]
            if sq.has_piece():
                return False
        # check along other diag
        for i, j in zip(range(row, len(brd.brd), 1),
                        range(col, -1, -1)):
            #            print(j,i)
            sq = brd.brd[i][j]
            if sq.has_piece():
                return False
        return True

    @staticmethod
    def Solve(board):
        """ Static method to solve a board. Ret: Boolean """
        global SOLVE
        i = 0

        while i < SOLVE[board.b_index]:
            if Board.SolveRemaining(board, 0) == False:
                print("No solution")
                return False

            # print solved out
            board.b_solved = True
            if CLI_MODE:
                print(board)

            # store in the solutions object
            Board.solutions[str(board.b_dims)+str(i)
                            ] = Board.recordsolution(board)

            if i < SOLVE[board.b_index] - 1:
                board.fresh_board()
                board.reset_move_count()
            i += 1
        # return board.b_solved

        return board.solutions

    @staticmethod
    def SolveRemaining(board, col):
        """ Recursive method for solving the n queens board. Ret: Boolean """
        if col >= board.b_dims:
            if Board.visited(board):
                return False
            return True

        for row in range(board.b_dims):
            Board.add_move(board)
            if Board.isSafe(board, row, col):
                square = board.brd[row][col]
                square.set_queen()
                if Board.SolveRemaining(board, col + 1) == True:
                    return True
                square.reset()
        return False

    @staticmethod
    def solved(sol, brd):
        """Helper method for debug mode"""
        print("Solved another board")
        print(Board.solutions[sol])

    @staticmethod
    def matches(board1, board2):
        """ Board 2 is an existing board and Board 1 is the new board """
        comp = Board.recordsolution(board1)
        for [i, j] in comp:
            if [i, j] not in board2:
                return False
        return True

    @staticmethod
    def visited(board):
        """Determines if a board is being revisited"""
        if len(board.solutions) == 0:
            return False
        for solved in board.solutions.values():
            if Board.matches(board, solved) == True:
                return True
        return False

    @staticmethod
    def recordsolution(board):
        """Enters a configuration of queens into the solutions map for that board"""
        s = []  # stores solution
        for j in range(board.b_dims):
            for i in range(board.b_dims):
                if board.brd[j][i].has_piece():
                    s.append([j, i])  # append file,rank to solution set
        return s

    def reset_move_count(self):
        """Resets the move count"""
        self.MOVES = 0

    def add_move(self):
        """Adds to the move count"""
        self.MOVES += 1

    def __repr__(self):
        """ Representation override method. Ret: String """
        my_repr = str(self.b_dims)+'-queens '
        if DEBUG:
            my_repr += "Data Representation:\n" + "".join(map(''.join, str(
                Game.games[self.id].brd))) + "\n"
        if self.b_solved:
            my_repr += "\nBoard Solved in %i moves!\n" % (self.MOVES)
            # transpose board to show file/rank A1 in lower left of CLI output
        if CLI_MODE:
            for i in range(self.b_dims):
                my_repr += '\n'
                # process
                for rank in self.brd:
                    my_repr += str(rank[self.b_dims-i-1]) + '\t'
        return my_repr

    @staticmethod
    def ShowSolution(solution):
        """Reads from the solution map and displays summary or CLI output"""
        summary = solution
        if CLI_MODE:
            summary = "Chessboard (CLI Mode):\n"
            b_dims = len(solution)
            rank = b_dims
            for i in range(b_dims):
                file = 'A'
                if i > 0:
                    rank -= 1
                    summary += "\n"
                for j in range(b_dims):
                    if j > 0:
                        file = chr(ord(file)+1)
                    summary += file + str(rank) + ':'
                    if [i, j] in solution:
                        summary += 'Qu'
                    summary += "\t"
            summary += "\n"
        return summary


def main():

    # new game
    g = Game()

    # uses the global tuple to setup "the boards"
    for b in BOARDS:
        g.new_game(Board(b))

    # solve each of "the boards"
    for uuid in g.games:
        b = g.fetch_board(uuid)
        Board.Solve(b)

    # show the summary output
    for s in Board.solutions.values():
        print(Board.ShowSolution(s))

    # with debug mode on changes to CLI_MODE to show last solved
    if DEBUG:
        global CLI_MODE
        CLI_MODE = True
        # print(g)
        print("\n\nLast used board ", end="")
        print(b)


main()
