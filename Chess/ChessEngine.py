"""
This class will store all info for current state and will help determine valid moves.It also keeps a move log
"""
class GameState:

    def __init__(self):
        #Board = 8*8 chessboard
        #each element has 2 characters
        #first character represents the color of the piece
        #second character represents the type of the piece
        #could use numpy arrays for better engine speed
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
    '''
        Takes a Move as a parameter and executes it, need to update it for castling, pawn promotion, en passant
    '''
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # logging the move to undo it later or to show the history fo the game
        self.whiteToMove = not self.whiteToMove # swap players
        # self.printBoard()
    '''
    Prints board in this state, for debugging
    '''
    def printBoard(self):
        """Prints the current board to the console"""
        for row in self.board:
            print(" ".join(row))
        print()  # blank line after the board


class Move:
    # maps keys to bales
    # key : value
    rank_row= {"1": 7,"2": 6,"3": 5,"4": 4,"5": 3,"6": 2,"7": 1,"8": 0,}
    files_cols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,}
    rowsToRanks = {v: k for k, v in rank_row.items()} # reversing dictionary without typing it completely
    colsToFiles = {v: k  for k, v in files_cols.items()} #same as above
    def __init__(self,startSq,endSq,board):
            self.startRow = startSq[0]
            self.startCol = startSq[1]
            self.endRow = endSq[0]
            self.endCol = endSq[1]
            self.pieceMoved = board[self.startRow][self.startCol]
            self.pieceCaptured = board[self.endRow][self.endCol]
    def getChessNotation(self):
        #make better notation later
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


