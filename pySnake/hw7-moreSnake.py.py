
# snake0.py

import random 
from Tkinter import *

def rgbString(red, green, blue): 
    return "#%02x%02x%02x" % (red, green, blue)

def mousePressed(canvas, event):
    if canvas.data.gameOver == False: #if the game isn't over
        canvas.data.xCoord = event.x #event.x is the x coordinate of the click
        canvas.data.yCoord = event.y #event.y is the y coordinate of the click 
        if canvas.data.isPaused == True and event.y > 50 and event.x > 5 and event.y < canvas.data.height-5 and event.x < canvas.data.width-5: #if the mouse click is within the margins of the board
            createWall(canvas)
        redrawAll(canvas)

def doTimerFired(canvas):
    ignoreThisTimerEvent = canvas.data.ignoreNextTimerEvent #sets whether this timer event has to be ignored 
    canvas.data.ignoreNextTimerEvent = False #the next timer event should not be ignored 
    if ignoreThisTimerEvent == False and canvas.data.gameOver == False:
        moveSnake(canvas, canvas.data.Drow, canvas.data.Dcol)
        redrawAll(canvas)

def timerFired(canvas):
    if canvas.data.isPaused == False:
        doTimerFired(canvas)
    if canvas.data.score < 3: #when the snake has eaten 3 food, it changes to lvl 2 with a faster speed 
        delay = 150 # milliseconds
    else:
        delay = 100
    def f():
        timerFired(canvas)
    canvas.after(delay, f) # pause, then call timerFired again

def sortHighscores(canvas): #sorts the high scores so they are displayed in order 
    canvas.data.highscores.sort()
    canvas.data.highscores.reverse()
    if len(canvas.data.highscores) > 3:
        canvas.data.highscores.pop()

def createWall(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if 5 + col*30 < canvas.data.xCoord <= 5 + (col+1)*30 and 5 + 50 + row*30 < canvas.data.yCoord <= 5 + 50 + (row+1)*30:
                if canvas.data.snakeBoard[row][col] != -1 and canvas.data.snakeBoard[row][col] != -2 and not canvas.data.snakeBoard[row][col] > 0: #looks for a value of row and col for which these conditions are true
                    if canvas.data.snakeBoard[row][col] == -3:
                        canvas.data.snakeBoard[row][col] = 0 #deletes the wall if one already exists on the clicked square
                    else:
                        canvas.data.snakeBoard[row][col] = -3 #sets the corresponding value of row and col in the snakeboard to -3 
                    break
    redrawAll(canvas)

def redrawAll(canvas):
    cx = canvas.data.width/2
    cy = canvas.data.height/2
    if canvas.data.gameOver == False:
        canvas.delete(ALL) #refreshes the board on each call of redrawALL  
    if (canvas.data.gameOver == True):
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
        canvas.data.highscores.append(canvas.data.score)
        sortHighscores(canvas)
        for i in xrange(len(canvas.data.highscores)):
            canvas.create_text(cx,cy+((i+1)*30), text = "Score " + str((i+1)*1) + ". " + str(canvas.data.highscores[i]), font = ("Helvetica", 18, "bold")) #displays the highscores
    canvas.create_text(cx,25,text = "Score: " + str(canvas.data.score), font = ("Helvetica", 18, "bold"))
    if canvas.data.gameOver == False:
        drawSnakeBoard(canvas)

def drawSnakeBoard(canvas):
    # you write this!
    # hint: for every row,col position on the board, call
    # drawSnakeCell, a helper method you will also write, like so
    #    drawSnakeCell(snakeBoard, row, col)
    board = canvas.data.snakeBoard
    rows = len(board)
    cols = len(board[0]) 
    for row in xrange(rows):
        for col in xrange(cols):
            drawSnakeCell(canvas,board,row,col)

def drawSnakeCell(canvas, snakeBoard, row, col):
    # you write this!
    # hint: place a margin 5-pixels-wide around the board.
    # make each cell 30x30
    # draw a white square and then, if the snake is in the
    # cell, draw a blue circle.
    margin = 5
    cellSize = 30
    left = margin + col * cellSize
    top = margin + row * cellSize
    canvas.create_rectangle(left, top + 50, left + cellSize, top + 50 + cellSize, fill = "white")
    if snakeBoard[row][col] > 0:
        if canvas.data.isPaused == False:
            canvas.create_oval(left, top + 50, left + cellSize, top + 50 + cellSize, fill = "blue") #creates each portion of the snake
        else:
            canvas.create_oval(left, top + 50, left + cellSize, top + 50 + cellSize, fill = rgbString(84,72,253)) #calls rbgString when the game is paused to display a lighter color
    if snakeBoard[row][col] == -1:
        if canvas.data.isPaused == False:
            canvas.create_oval(left, top + 50, left + cellSize, top + 50 + cellSize, fill = "green") #creates the food 
        else:
            canvas.create_oval(left, top + 50, left + cellSize, top + 50 + cellSize, fill = rgbString(96,253,72))
    if snakeBoard[row][col] == -2:
        if canvas.data.isPaused == False:
            canvas.create_oval(left, top + 50, left + cellSize, top + 50 + cellSize, fill = "red") #creates the poison
        else:
            canvas.create_oval(left, top + 50, left + cellSize, top + 50 + cellSize, fill = rgbString(255,60,60))
    if snakeBoard[row][col] == -3:
        if canvas.data.isPaused == False:
            canvas.create_rectangle(left, top + 50, left + cellSize, top + 50 + cellSize, fill = "brown") #creates the walls
        else:
            canvas.create_rectangle(left, top + 50, left + cellSize, top + 50 + cellSize, fill = rgbString(208,119,67))

        
def loadSnakeBoard(canvas):
    # you write this!
    # allocate the new snakeBoard 2d list as described
    # in the notes, and store it in the canvas's data
    rows = canvas.data.rows
    cols = canvas.data.cols
    board = []
    for row in xrange(rows):
        board += [[0]*cols]
    board[rows/2][cols/2] = 1
    canvas.data.snakeBoard = board
    canvas.data.ignoreNextTimerEvent = False
    placeFood(canvas) 
    findSnakeHead(canvas)

def keyPressed(canvas, event):
    canvas.data.ignoreNextTimerEvent = True
    if (event.char == "q") and canvas.data.gameOver == False:
        gameOver(canvas)
        redrawAll(canvas)
    elif (event.char == "r"):
        init(canvas)
    if canvas.data.gameOver == False:
        if (event.char == "p"):
            canvas.data.isPaused = not canvas.data.isPaused
        if event.keysym == "Up":
            canvas.data.moves += 1
            moveSnake(canvas,-1,0)
        if event.keysym == "Down":
            canvas.data.moves += 1
            moveSnake(canvas,1,0)
        if event.keysym == "Left":
            canvas.data.moves += 1
            moveSnake(canvas,0,-1)
        if event.keysym == "Right":
            moveSnake(canvas,0,1)
        redrawAll(canvas)

def removeTail(canvas): #removes the last portion of the snake by subtracting 1 from each element in the snakeboard greater than 0 
    for rows in xrange(canvas.data.rows):
        for cols in xrange(canvas.data.cols):
            if canvas.data.snakeBoard[rows][cols] > 0:
                canvas.data.snakeBoard[rows][cols] -= 1

def moveSnake(canvas, drow, dcol):
    canvas.data.Drow = drow #sets the direction the snake is moving in 
    canvas.data.Dcol = dcol 
    headRow = canvas.data.headRow
    headCol = canvas.data.headCol
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    if newHeadRow >= canvas.data.rows or newHeadRow < 0 or newHeadCol >= canvas.data.cols or newHeadCol < 0: #if the snake collides with the sides of the board
        gameOver(canvas)
    elif canvas.data.snakeBoard[newHeadRow][newHeadCol] == -3: #if the snake collides with a wall 
        canvas.data.score -= 1
        canvas.data.snakeBoard[newHeadRow][newHeadCol] == 0
        if canvas.data.score < 0:
            gameOver(canvas)
    if newHeadRow >= canvas.data.rows or newHeadRow < 0 or newHeadCol >= canvas.data.cols or newHeadCol < 0:  
        gameOver(canvas)
    elif canvas.data.snakeBoard[newHeadRow][newHeadCol] > 0: #if the snake collides with itself
        gameOver(canvas)
    elif canvas.data.snakeBoard[newHeadRow][newHeadCol] == -2: #if the snake collides with poison 
        gameOver(canvas)
    elif canvas.data.snakeBoard[newHeadRow][newHeadCol] == -1: #if the snake collides with food 
        canvas.data.snakeBoard[newHeadRow][newHeadCol] = 1 + canvas.data.snakeBoard[headRow][headCol]
        canvas.data.headRow = newHeadRow
        canvas.data.headCol = newHeadCol
        canvas.data.score += 1
        placeFood(canvas)
        if canvas.data.moves >= 20 and wallsPresent(canvas) == True:
            canvas.data.score += 1
        if canvas.data.score >=3:
            placePoison(canvas)
        canvas.data.moves = 0 
    else:
        canvas.data.snakeBoard[newHeadRow][newHeadCol] = 1 + canvas.data.snakeBoard[headRow][headCol]
        canvas.data.headRow = newHeadRow
        canvas.data.headCol = newHeadCol
        removeTail(canvas)

def wallsPresent(canvas): #checks if there are walls present on the board 
    for rows in xrange(canvas.data.rows):
        for cols in xrange(canvas.data.cols):
            if canvas.data.snakeBoard[rows][cols] == -3:
                return True
    return False
                
    
def placeFood(canvas): #places food randomly where there is no snake, poison or wall 
    while True:
        randomRow = random.randint(0,canvas.data.rows - 1)
        randomCol = random.randint(0,canvas.data.cols - 1)
        if not canvas.data.snakeBoard[randomRow][randomCol] > 0:
            if not canvas.data.snakeBoard[randomRow][randomCol] == -2:
                if not canvas.data.snakeBoard[randomRow][randomCol] == -3:
                    canvas.data.snakeBoard[randomRow][randomCol] = -1
                    break

def placePoison(canvas): #places poison where there is no snake, food or wall 
    while True:
        randomRow = random.randint(0,canvas.data.rows - 1)
        randomCol = random.randint(0,canvas.data.cols - 1)
        if not canvas.data.snakeBoard[randomRow][randomCol] > 0:
            if not canvas.data.snakeBoard[randomRow][randomCol] == -1:
                if not canvas.data.snakeBoard[randomRow][randomCol] == -3:
                    if randomRow + 1 != canvas.data.headRow and randomRow - 1 != canvas.data.headRow:
                        if randomCol + 1 != canvas.data.headCol and randomCol - 1 != canvas.data.headCol:
                            canvas.data.snakeBoard[randomRow][randomCol] = -2
                            break

def gameOver(canvas):
    canvas.data.gameOver = True
    
def findSnakeHead(canvas): #finds the row and column where the head of the snake is 
    highest = 0
    location = [0,0]
    for rows in xrange(canvas.data.rows):
        for cols in xrange(canvas.data.cols):
            if canvas.data.snakeBoard[rows][cols] > highest:
                highest = canvas.data.snakeBoard[rows][cols]
                location = [rows,cols]
    canvas.data.headRow = location[0]
    canvas.data.headCol = location[1]
    
def printInstructions():
    print """Snake!
             Use the arrow keys to move the snake.
             Eat food to grow.
             Stay on the board!
             And don't crash into yourself!""" 

def init(canvas):
    printInstructions()
    loadSnakeBoard(canvas)
    canvas.data.gameOver = False 
    canvas.data.Drow = 0
    canvas.data.Dcol = -1
    canvas.data.score = 0
    canvas.data.moves = 0 
    redrawAll(canvas)

def run(rows,cols):
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=cols*30+10, height=rows*30+10+50)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.width = cols*30+10
    canvas.data.height= rows*30+10+50 
    canvas.data.gameOver = False
    canvas.data.isPaused = False
    canvas.data.ignoreNextTimerEvent = False
    canvas.data.headRow = 0
    canvas.data.headCol = 0
    canvas.data.highscores = [] 
    init(canvas)
    # set up events
    root.bind("<Button-1>", lambda event: mousePressed(canvas, event))
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run(15,15)
