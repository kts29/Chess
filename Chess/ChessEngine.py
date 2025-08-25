"""
This class will store all info for current state and will help determine valid moves.It also keeps a move log
"""
class GameState():

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
