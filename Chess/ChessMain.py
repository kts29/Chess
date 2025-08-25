"""
This is our main driver file. It is responsible for handling user input and displaying the current GameState object
"""

import pygame as p
from Chess import ChessEngine

WIDTH = 512
HEIGHT  = 512 #400 is also okay, 512 is good as it's a power of 2
DIMENSION = 8 #Dimensions of a chessboard are 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called once in the main
"""

def loadImages():
    pieces = ['wp','wR','wB','wN','wQ','wK','bp','bR','bB','bN','bQ','bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )

    #Note: we can get our image from images at all times by saying IMAGES['wp']
'''
The main driver for our code. This will basically handle I/O (user input and updating the graphics)
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    loadImages() #only do this once
    running = True
    sqSelected = () # no square is initially selected, keeps track of the last click of the user
    playerClicks = [] # keep track of player clicks (two tuples: [(x0,y0),(x1,y1)])
    drawGameState(screen, gs)
    while running:
        drawGameState(screen, gs)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row,col): # user selected same square twice
                    sqSelected = () #deselect
                    playerClicks = [] # clear player clicks, removes history as it's not needed
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks)  == 2: #action after start and end square selected
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #reset user clicks
                    playerClicks = [] #reset Player Clicks
            clock.tick(MAX_FPS)
            p.display.flip()

'''
Responsible for the graphics within a current game state
'''
def drawGameState(screen,gs):
    drawBoard(screen) #draw squares on the board
    #add in piece highlighting or move suggestions
    drawPieces(screen,gs.board)
'''
Draw squares on the board, top left square is always light.
'''
def drawBoard(screen):
    colors = [p.Color('white'),p.Color('gray')]
    for row in range (DIMENSION):
        for col in range (DIMENSION):
            color = colors[(row+col)%2]
            p.draw.rect(screen,color,p.Rect(row*SQ_SIZE,col*SQ_SIZE,SQ_SIZE,SQ_SIZE))



'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen,board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece],p.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))

if __name__ == '__main__':
    # Good practice in Python:
    # - When run directly as a script, this block executes the program’s main logic.
    # - When imported as a module, all global variables, functions, and classes are still
    #   defined and available, and any top-level statements are executed,
    #   but the main() function is not called automatically.
    # - This avoids unwanted side effects during imports, while still allowing reuse.
    main()