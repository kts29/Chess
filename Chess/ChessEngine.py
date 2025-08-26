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
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunction = {'P' : self.getPawnMoves, 'N' : self.getKnightMoves,'B' : self.getBishopMoves,
                             'Q':self.getQueenMoves,'K' : self.getKingMoves,'R' : self.getRookMoves}

    def notValidSquare(self, row, col, sqSelected, playerClicks):
        """
        Checks whether the selected square is invalid for the current player.
        Conditions:
          1. Player clicked the same square again.
          2. First click is on an empty square or on the opponent's piece.
        """
        return (
                sqSelected == (row, col) or
                (
                        playerClicks.count == 0 and (
                        self.board[row][col] == '--' or
                        (self.board[row][col][0] == 'b' and self.whiteToMove) or
                        (self.board[row][col][0] == 'w' and not self.whiteToMove)
                )
                )
        )

    def makeMove(self,move):
        """
        Takes a Move as a parameter and executes it, need to update it for castling, pawn promotion, en passant
        """
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # logging the move to undo it later or to show the history fo the game
        self.whiteToMove = not self.whiteToMove # swap players
        # self.printBoard()
    '''
    Prints board in the current state, for debugging
    '''
    def printBoard(self):
        for row in self.board:
            print(" ".join(row))
        print()  # blank line after the board

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove


    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getPossibleMoves() # for now lets not worry about it
    '''
    All moves not considering checks
    '''
    def getPossibleMoves(self):
        moves = []
        for r in range (len(self.board)): # number of rows
            for c in range (len(self.board[r])): #number of cols in given row
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r,c,moves)
        return moves
    '''
    Get all Pawn Moves for the pawn located at row,col and add these moves to the list
    Unique because black and white pawns behave differently
    '''
    def getPawnMoves(self, r, c, moves):
        '''
        Handle en passant and promotion later
        '''
        if self.whiteToMove:
            # Handle all normal pawn moves
            if self.board[r-1][c] == '--':
                moves.append( Move((r,c),(r-1,c),self.board) )
                if r == 6 and self.board[r - 2][c] == '--':
                    moves.append( Move((r,c),(r-2,c),self.board))
            if c - 1 >= 0: #captures on the left
                if self.board[r-1][c-1][0] == 'b':
                    moves.append( Move((r,c),(r-1,c-1),self.board))
            if c + 1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append( Move((r,c),(r-1,c+1),self.board))

        if not self.whiteToMove:
            if self.board[r+1][c] == '--':
                moves.append( Move((r,c),(r+1,c),self.board) )
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append( Move((r,c),(r + 2,c),self.board))
            if c - 1 >= 0:  # captures on the left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to the right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))



    '''
    Get all rook Moves for the rook located at row,col and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        # Handle all rook moves
        enemyPieceIndicator = 'b' if self.whiteToMove else 'w'
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in directions:
            i = 1
            new_r = r + dr
            new_c = c + dc
            while 0 <= new_r < len(self.board) and 0 <= new_c < len(self.board[r]): #check if its in loop
                curr = self.board[new_r][new_c]
                if curr == '--' or curr[0] == enemyPieceIndicator:
                    moves.append(Move((r, c), (new_r,new_c), self.board)) # make either normal move or capture
                    if curr[0] == enemyPieceIndicator:  # make the move and stop the loop
                        break
                else:
                    break
                i += 1
                new_r += dr
                new_c += dc

    def getKnightMoves(self,r,c,moves):
        enemyPieceIndicator = 'b' if self.whiteToMove else 'w'
        # directions = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
        directions2 = [(1,2),(2,1)]

        for dr, dc in directions2:
            for sign1 in(-1,1):
                for sign2 in (-1,1):
                    new_r = r + sign1*dr
                    new_c = c + sign2*dc
                    if 0 <= new_r < len(self.board) and 0 <= new_c < len(self.board[r]):  # check if its in board
                        curr = self.board[new_r][new_c]
                        if curr == '--' or curr[0] == enemyPieceIndicator:
                            moves.append(Move((r, c), (new_r, new_c), self.board))  # make either normal move or capture


    def getBishopMoves(self,r,c,moves):
        enemyPieceIndicator = 'b' if self.whiteToMove else 'w'
        for sign1 in (-1,1):
            for sign2 in (-1,1):
                new_r = r + sign1
                new_c = c + sign2
                while 0 <= new_r < len(self.board) and 0 <= new_c < len(self.board[r]):  # check if its in loop
                    curr = self.board[new_r][new_c]
                    if curr == '--' or curr[0] == enemyPieceIndicator:
                        moves.append(Move((r, c), (new_r, new_c), self.board))  # make either normal move or capture
                        if curr[0] == enemyPieceIndicator:  # make the move and stop the loop
                            break
                    else:
                        break
                    new_r += sign1
                    new_c += sign2


    def getKingMoves(self,r,c,moves):
        enemyPieceIndicator = 'b' if self.whiteToMove else 'w'
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr == dc == 0: continue
                new_r = r + dr
                new_c = c + dc
                if 0 <= new_r < len(self.board) and 0 <= new_c < len(self.board[r]):  # check if its in loop
                    curr = self.board[new_r][new_c]
                    if curr == '--' or curr[0] == enemyPieceIndicator:
                        moves.append(Move((r, c), (new_r, new_c), self.board))


    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r, c,moves)
        self.getBishopMoves(r, c, moves)


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
            self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol # all moves have a unique moveID (hash function)
            # print(self.moveID)
    '''
    Overriding the equals method
    '''
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        #make better notation later
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

# class EnPassant(Move):
#     def __init__(self,startSq,endSq,board):

