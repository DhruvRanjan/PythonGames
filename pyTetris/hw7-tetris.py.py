# events-example0.py

from Tkinter import *
import random 

def mousePressed(canvas, event):
    redrawAll(canvas)

def keyPressed(canvas, event): 
    if event.char == "r":
        init(canvas)
    if canvas.data.canRotate == True: #ensures that a piece isnt rotated while it's being placed 
        if event.keysym == "Up":
            rotateFallingPiece(canvas)
    if event.keysym == "Down":
        moveFallingPiece(canvas,1,0)
    elif event.keysym == "Left":
        moveFallingPiece(canvas,0,-1)
    elif event.keysym == "Right":
        moveFallingPiece(canvas,0,1)
    redrawAll(canvas)
    
def timerFired(canvas):
    if moveFallingPiece(canvas,+1,0) == False: #if the piece cannot fall any further
        canvas.data.canRotate = False
        placeFallingPiece(canvas)
        newFallingPiece(canvas)
        canvas.data.canRotate = True 
        if fallingPieceIsLegal(canvas) == False:
            canvas.data.isGameOver = True
    redrawAll(canvas)
    delay = 300 # milliseconds
    def f():
        timerFired(canvas)
    canvas.after(delay, f) # pause, then call timerFired again

def redrawAll(canvas): #draws ALL OF THE THINGS 
    removeFullRows(canvas)
    canvas.delete(ALL)
    if (canvas.data.isGameOver == True):
        cx = canvas.data.width/2
        cy = canvas.data.height/2
        canvas.create_text(cx+25, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
        canvas.create_text(cx+25, cy+100, text="Press r to restart", font=("Helvetica", 28, "bold"))
    if canvas.data.isGameOver == False:
        drawBoard(canvas)
        drawFallingPiece(canvas)
    canvas.create_text(canvas.data.width/2 + 10, 30, text = "Score: " + str(canvas.data.score), font = ("Helvetica", 18, "bold")) #displays the score

def drawBoard(canvas):
    board = canvas.data.tetrisBoard
    rows = len(board)
    cols = len(board[0])
    canvas.create_rectangle(0,0,canvas.data.width+100,canvas.data.height+200,fill="orange") #+100 and +200 because of the borders
    for row in xrange(rows):
        for col in xrange(cols):
            color = board[row][col]
            drawTetrisCell(canvas,row,col,color)

    

def drawTetrisCell(canvas,row,col,color):
    margin = 50
    cellSize = 30
    left = margin + col * cellSize
    top = margin + row * cellSize
    canvas.create_rectangle(left, top, left + cellSize, top + cellSize, fill = "black") #makes the black margin around each cell 
    canvas.create_rectangle(left+2, top+2, left + cellSize-2, top + cellSize-2, fill = color)

def loadBoard(canvas):
    board = []
    for rows in xrange(canvas.data.rows):
        board += [[canvas.data.emptyColor]*canvas.data.cols]
    canvas.data.tetrisBoard = board


def newFallingPiece(canvas):
    piece_index = random.randint(0,len(canvas.data.tetrisPieces)-1)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[piece_index]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[piece_index]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 - len(canvas.data.fallingPiece[0])/2 #finds the column of the falling piece

def drawFallingPiece(canvas):
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    rowOffshift = canvas.data.fallingPieceRow
    colOffshift = canvas.data.fallingPieceCol
    for row in xrange(rows):
        for col in xrange(cols):
            if canvas.data.fallingPiece[row][col] == True:
                drawTetrisCell(canvas,rowOffshift + row,colOffshift+col,canvas.data.fallingPieceColor) #the offshift corresponds to the initial row/col of the falling piece

def placeFallingPiece(canvas): #places the falling piece on the board if it cannot fall any further 
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    rowOffshift = canvas.data.fallingPieceRow
    colOffshift = canvas.data.fallingPieceCol
    for row in xrange(rows):
        for col in xrange(cols):
            if canvas.data.fallingPiece[row][col] == True:
                canvas.data.tetrisBoard[rowOffshift + row][colOffshift+col] = canvas.data.fallingPieceColor
    removeFullRows(canvas)
                
def moveFallingPiece(canvas,drow,dcol): #drow and dcol correspond to the direction the piece is moving in 
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if not fallingPieceIsLegal(canvas) == True:
        canvas.data.fallingPieceRow -= drow
        canvas.data.fallingPieceCol -= dcol
        return False
    return True

def checkRowIsFull(canvas,row):
    for element in xrange(len(canvas.data.tetrisBoard[row])):
       if canvas.data.tetrisBoard[row][element] == canvas.data.emptyColor: #if a single cell is == emptyColor, the row cannot be full 
           return False
    return True

def removeFullRows(canvas): #copies all of the non-full rows into a new array, and then this array becomes canvas.data.tetrisBoard
    newRow = canvas.data.rows - 1 
    fullRows = 0 
    for oldRow in xrange(canvas.data.rows-1,-1,-1):
        row = canvas.data.tetrisBoard[oldRow]
        if checkRowIsFull(canvas,oldRow) == False:
            for cols in xrange(canvas.data.cols):
                canvas.data.tetrisBoard[newRow][cols] = canvas.data.tetrisBoard[oldRow][cols]
            newRow -= 1
        else:
            fullRows += 1
    canvas.data.score += fullRows**2 #the score is equal to the square of the number of rows removed at once
                
def fallingPieceIsLegal(canvas):
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    rowOffShift = canvas.data.fallingPieceRow
    colOffShift = canvas.data.fallingPieceCol
    for row in xrange(rows):
        for col in xrange(cols):
            if canvas.data.fallingPiece[row][col] == True:
                if row + rowOffShift >= canvas.data.rows or row+rowOffShift < 0 or col + colOffShift >= canvas.data.cols or col+colOffShift < 0: #checks if the piece is off the board
                    return False
                if canvas.data.tetrisBoard[row+rowOffShift][col+colOffShift] != canvas.data.emptyColor: #
                    return False
    return True

def rotateFallingPiece(canvas):
    fallingRow = canvas.data.fallingPieceRow
    fallingCol = canvas.data.fallingPieceCol
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    newRows = cols
    newCols = rows
    piece = canvas.data.fallingPiece
    new_piece = []
    i = len(canvas.data.fallingPiece[0])-1
    while i >= 0: #rotates the piece differently depending on the number of rows and columns 
        if rows == 4:
            new_piece+= [[canvas.data.fallingPiece[0][i],canvas.data.fallingPiece[1][i],canvas.data.fallingPiece[2][i],canvas.data.fallingPiece[3][i]]]
        elif rows == 3:
            new_piece+= [[canvas.data.fallingPiece[0][i],canvas.data.fallingPiece[1][i],canvas.data.fallingPiece[2][i]]]
        elif rows == 2:
            new_piece+=[[canvas.data.fallingPiece[0][i],canvas.data.fallingPiece[1][i]]]
        else:
            new_piece+=[[canvas.data.fallingPiece[0][i]]]
        i -= 1
    if len(canvas.data.fallingPiece) == 1:
        canvas.data.fallingPieceCol += 1
    elif len(canvas.data.fallingPiece) == 4:
        canvas.data.fallingPieceCol -= 1
    canvas.data.fallingPiece = new_piece
    if not fallingPieceIsLegal(canvas):
        canvas.data.fallingPiece = piece
        if len(canvas.data.fallingPiece) == 1:
            canvas.data.fallingPieceCol -= 1
        elif len(canvas.data.fallingPiece) == 4:
            canvas.data.fallingPieceCol += 1
    new_piece = []
    
            
def init(canvas): #sets the array of each individual piece and starts the game 
    iPiece = [
    [ True,  True,  True,  True]
    ]
  
    jPiece = [
    [ True, False, False ],
    [ True, True,  True]
    ]
  
    lPiece = [
    [ False, False, True],
    [ True,  True,  True]
    ]
  
    oPiece = [
    [ True, True],
    [ True, True]
    ]
  
    sPiece = [
    [ False, True, True],
    [ True,  True, False ]
    ]
  
    tPiece = [
    [ False, True, False ],
    [ True,  True, True]
    ]

    zPiece = [
    [ True,  True, False ],
    [ False, True, True]
    ]
    
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    canvas.data.tetrisPieces = tetrisPieces
    canvas.data.tetrisPieceColors = tetrisPieceColors
    canvas.data.canRotate = True 
    canvas.data.isGameOver = False
    canvas.data.score = 0
    loadBoard(canvas)
    newFallingPiece(canvas)
    redrawAll(canvas)

def run(rows,cols):
    # create the root and the canvas
    margin = 50
    cellsize = 30
    root = Tk()
    canvas = Canvas(root, width=cols*cellsize+100, height=rows*cellsize+100)#add 2 times the cellsize to account for the orange margin
    canvas.pack()
    root.resizable(width=0, height=0)
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.emptyColor = "blue"
    canvas.data.width = cols*cellsize+50
    canvas.data.height = cols*cellsize+50
    init(canvas)
    # set up events
    root.bind("<Button-1>", lambda event: mousePressed(canvas, event))
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)


run(15,10)
