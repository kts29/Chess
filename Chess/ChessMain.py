"""
This is our main driver file. It is responsible for handling user input and displaying the current GameState object
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT  = 950 #400 is also okay, 512 is good as it's a power of 2
DIMENSION = 8 #Dimensions of a chessboard are 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
The main driver for our code. This will basically handle I/O (user input and updating the graphics)
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    newMoveMade = False # Flag variable that tells us a new move has been made and validMoves has to be regenerated

    loadImages() #only do this once
    running = True
    sqSelected = () # no square is initially selected, keeps track of the last click of the user
    playerClicks = [] # keep track of player clicks (two tuples: [(x0,y0),(x1,y1)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row,col): # user selected same square twice or wrong color piece
                    sqSelected = () #deselect
                    playerClicks = [] # clear player clicks, removes history as it's not needed
                else:
                    sqSelected = (row, col)
                    # if gs.board[playerClicks[0][0]][playerClicks[0][1]][0] == gs.board[playerClicks[1][0]][playerClicks[1][1]][0]:
                    #     #checks whether the player has switched pieces rather than playing a move
                    #     playerClicks = [] #before appending sqSelected just make clear it so the next non-white piece selected counts as the move
                    playerClicks.append(sqSelected)
                if len(playerClicks)  == 2: #action after start and end square selected
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    for i_move in range(len(validMoves)): #changed this from for moves in validMoves because my moves now have more information that just starting and ending square, we now have flags for enpassant and castling and because these exist I want to makeMove(validMoves[i]) because it is generated and will have the flags checked and set/reset
                        if move == validMoves[i_move]: #This works because my comparator is based on moveID which depends on initial and final clicks only and not flags
                            newMoveMade = True
                            gs.makeMove(validMoves[i_move]) #Now I am not making the move which only has st and end sq specified , I also have the flags set/reset
                            sqSelected = () #reset user clicks
                            playerClicks = [] #reset Player Clicks
                    if not newMoveMade:
                        playerClicks = [sqSelected]
                    # else:
                    #     gs.printBoard()

                print(playerClicks)
                print(gs.whiteToMove)
            # key handles
            elif e.type == p.KEYDOWN :
                if e.key == p.K_z:
                    gs.undoMove()
                    newMoveMade = True # logically a move has been made and the flag should be changes
                print(playerClicks)
        if newMoveMade:
            validMoves = gs.getValidMoves()
            newMoveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Initialize a global dictionary of images. This will be called once in the main
"""

def loadImages():
    pieces = ['wP','wR','wB','wN','wQ','wK','bP','bR','bB','bN','bQ','bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )

    #Note: we can get our image from images at all times by saying IMAGES['wP']

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

# def delay():
#     p.time.delay(100)

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