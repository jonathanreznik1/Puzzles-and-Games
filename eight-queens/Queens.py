import uuid
import sys

#PROJECT TODO LIST: 
# 1) Queens.py
#   a. simplify the program
#   b. remove global vars if possible
#   c. cleanup the unused functions
# 2) QtGame.py
#   a. introduce gui elements
#   b. Interactive cycling through the solutions
# 3) Solutions.py
#   a. Implement Backtracking algorithm
#   b. Compare the efficiency of the two algorithms
#   c. Expand on solutions introducing concurrency
# 4) Other
#   a.  using a file to store or check solutions
#   b.  Create HINT feature with some AI or greedy algorithm

# python 8 queens problem
DEBUG = True
MOVE_DEBUG = True
CLI_MODE = False
MODE_GAME = 2


class Piece():
    def __init__(self, chesspiece, file, rank, board):
        self.b_id = board.b_id
        self.p_location = (file,rank)
        self.p_type = chesspiece
    
    '''Assign piece to a square.        Args: self, square         Returns: None   
        '''
    def set_square(self, square):
        square.piece = self
        
    '''Moves piece to an empty square.        Args: self, square        Returns:  (x,y) location '''
    def move_queen(self,square):
    
        #Get the Board
        B = Game.fetch_board(self)          
        # B = games[self.b_id]
        x,y = square.get_location()
        sqr = Board.fetch_square(B.brd,x,y)

        #Check for piece and raise exception if so
        if not sqr.has_piece():
            
            #Store the current location in sq
            file = self.p_location[0]
            rank = self.p_location[1]
            sq = B.brd[file][rank]
            
            #Move piece and add to move history
            self.set_square(B.brd[x][y])
            Game.move_history[self.b_id].append([self.p_type,self.p_location,(x,y)])
            self.p_location = (x,y)

            #Cleanup the old square and return the new location
            sq.reset_piece()
            return self.p_location
            
        else:
            raise Exception("Illegal Move, piece already exists there.")
            return False  
    
    '''String override method'''
    def __str__(self):
        if self.p_type is "QUEEN":
            return "Qu"
        

class Square():
    def __init__(self, board, rank, file):
        self.b_id = board.b_id
        self.piece = Piece(None,file,rank,board)
        self.location = (rank, file)                     #rank location[0], file location[1]

    def has_piece(self):
        if self.piece.p_type is None:
            return False
        return True

    def reset_piece(self):
        self.piece = Piece(None,self.location[1],self.location[0],Game.fetch_board(self))
        
    def get_piece(self):
        return self.piece
       
    '''Show rank of square        Args: self        Returns: integer value from 1 to b_size '''
    def get_rank(self):
        return self.get_board_size() - self.location[0]

    '''Show file of square        Args: self        Returns: character from A to ?'''
    def get_file(self):
        return chr(ord('A')+self.location[1])
                
    def get_location(self):
        return self.location[0],self.location[1]

    def __str__(self):
        if self.piece.p_type is None:
            return ""
        return "%s%s" % (self.location[1], self.location[0]) + ":" + "%s\t" % (self.piece)

    def __repr__(self):
        if self.has_piece():
            return self.piece.p_type
        return "Square"
        
class Board():
    def __init__(self, dimensions):
        self.b_dim = dimensions
        self.b_solved = False
        self.b_id = uuid.uuid1()        #assigns a unique id
        self.brd = [[Square(self,i,j) for j in range(dimensions)] for i in range(dimensions)]       

    '''The static Board.fetch_square() method returns a Square object'''
    @staticmethod
    def fetch_square(board,rank,file):
        return board[rank][file]
    
    '''The static Board.setup_queens() method places Queen pieces on the diagonal of squares'''
    @staticmethod
    def setup_queens(board):
        for i,item in enumerate(board.brd):
            item[0].piece = Piece("QUEEN",i,i,board)

    def __repr__(self):
        my_repr = ''
        chess_repr = "Chessboard (CLI) Representation:\n"
        if self.b_solved:
            chess_repr += "Board Solved!\n"
        rank = self.b_dim
        for i in range(self.b_dim):
            file = 'A'
            if i > 0:
                rank -= 1
                chess_repr += "\n"
            for j in range(self.b_dim):
                if j > 0:
                    file = chr(ord(file) + 1)
                chess_repr += file + str(rank) +':'+ str(self.brd[i][j])[-3:-1]+"\t"
        chess_repr += "\n"
        my_repr += chess_repr
        if DEBUG:
            my_repr += "Data Representation:\n" + "".join(map(''.join,str(Game.games[self.b_id].brd))) + "\n"
        if MOVE_DEBUG:
            my_repr += "Game Move Representation:\n" + "".join(str(x) for x in Game.move_history[self.b_id])
        return my_repr
        
class Game():
    games = dict()
    move_history = {}

    def __init__(self):
        self.b_game_mode = MODE_GAME    # 1,2  for auto/interactive

    '''The static Game.fetch_board() method returns a Board object'''
    @staticmethod
    def fetch_board(item):
        return Game.games[item.b_id] 
        
    def new_game(self,board):
        if DEBUG:
            print("newboard: " + str(board.b_id))
        
        self.games[board.b_id] = board           #map board to games

        self.move_history[board.b_id] = []


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
    for uuid in g.games.values():
        print(g.fetch_board(uuid))

    #Call setup_queens()
    for uuid in g.games.values():
        Board.setup_queens(g.fetch_board(uuid))
        print(g.fetch_board(uuid))

        

#######     TESTING     ######################
# #for Queen Gamepiece placement           # #
##############################################

    #Test of removal or addition of pieces  
    #N/A

    #Test of allowable moves
    for uuid in g.games.values():
        brd = g.fetch_board(uuid)
        sqr = Board.fetch_square(brd.brd,0,0)
        if sqr.has_piece():
            piece = sqr.get_piece()
            if Board.fetch_square(brd.brd,0,6).has_piece():
                raise Exception('not a legal move')
            else:
                piece.move_queen(Board.fetch_square(brd.brd,0,6))

    for board in g.games.values():
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

