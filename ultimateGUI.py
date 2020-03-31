import tictactoe
import random
import minimax
from graphics import *

def evalFn(gameState):
	return float('inf')*gameState.getWinner() + sum(sum(wins) for wins in gameState.getMiniWins())


# clicking the Step button will check to see if a legal move was made
def getButtonClick(window):
    window.update()      # flush any prior clicks
    window.mouseX = None
    window.mouseY = None
    # checks if the button in the bottom right corner has been pressed
    while window.mouseX == None or window.mouseY == None or not (window.mouseX < 400 and window.mouseX > 350 and window.mouseY > 350 and window.mouseY < 400):
        window.update()
        if window.isClosed(): raise GraphicsError("getMouse in closed window")
        time.sleep(.1) # give up thread
    x,y = window.toWorld(window.mouseX, window.mouseY)
    window.mouseX = None
    window.mouseY = None
    return Point(x,y)

def drawBoard(window, x1, y1, x2, y2):
	l1 = Line(Point(x1 + (x2 - x1)/3.0, y1), Point(x1 + (x2 - x1)/3.0, y2))
	l1.draw(window)
	l2 = Line(Point(x1 + 2*(x2 - x1)/3.0, y1), Point(x1 + 2*(x2 - x1)/3.0, y2))
	l2.draw(window)
	l3 = Line(Point(x1, y1 + (y2 - y1)/3.0), Point(x2, y1 + (y2 - y1)/3.0))
	l3.draw(window)
	l4 = Line(Point(x1, y1 + 2*(y2 - y1)/3.0), Point(x2, y1 + 2*(y2 - y1)/3.0))
	l4.draw(window)

def drawRect(window, x1, y1, x2, y2):
	l1 = Line(Point(x1, y1), Point(x2, y1))
	l1.draw(window)
	l2 = Line(Point(x2, y1), Point(x2, y2))
	l2.draw(window)
	l3 = Line(Point(x1, y1), Point(x1, y2))
	l3.draw(window)
	l4 = Line(Point(x1, y2), Point(x2, y2))
	l4.draw(window)


agent = minimax.AlphaBetaAgent(evalFn, 2)
window = GraphWin("Ultimate Tic-Tac-Toe", 400, 400)
window.setBackground(color_rgb(255, 255, 255))

myGame = tictactoe.Game()
# keep track of the entries and replaces them with text boxes 
cells = [[] for i in range(myGame.dim**2)]
# keeps track of the X's and the O's ('-' refers to nothing)
inputs = [['-' for j in range(myGame.dim**2) ] for i in range(myGame.dim**2)]

# print inputs

# should be at least 25
dist = 25
rectDist = 90
space = 10

for r in range(myGame.dim):
	for c in range(myGame.dim):
		topLeft = (10 + r*rectDist + space*(r % 3), 10 + c*rectDist + space*(c % 3))
		topRight = (topLeft[0] + rectDist, topLeft[1])
		botLeft = (topLeft[0], topLeft[1] + rectDist)
		botRight = (topLeft[0] + rectDist, topLeft[1] + rectDist)
		l1 = Line(Point(topLeft[0], topLeft[1]), Point(topRight[0], topRight[1]))
		l1.draw(window)
		l2 = Line(Point(botRight[0], botRight[1]), Point(topRight[0], topRight[1]))
		l2.draw(window)
		l3 = Line(Point(botRight[0], botRight[1]), Point(botLeft[0], botLeft[1]))
		l3.draw(window)
		l4 = Line(Point(topLeft[0], topLeft[1]), Point(botLeft[0], botLeft[1]))
		l4.draw(window)

# set up text boxes for input
for r in range(myGame.dim**2):
	for c in range(myGame.dim**2):
		e = Entry(Point(dist*r + dist + (r/3)*dist + 5*(r%3), dist*c + dist + (c/3)*dist + 5*(c%3)), dist/10)
		e.draw(window)
		cells[r].append(e)

# box to confirm a move/verify a move
drawRect(window, 350, 350, 400, 400)
t = Text(Point(375, 375), 'Step')
t.draw(window)

# find the one legal move. Returns (-1, -1) when there are multiple moves
def findMove():
	x = -1
	y = -1
	for r in range(myGame.dim**2):
		for c in range(myGame.dim**2):
			cur = cells[r][c]
			if cur != None:
				# print cur.getText()
				if cur.getText() == 'x':
					if x == -1 and y == -1:
						x = r
						y = c
					else:
						return (-1, -1)
				elif cur.getText() != "":
					return (-1, -1)
	return (x, y)


# play game
myGame.currPlayer = 1
# help keep track of current player
count = 0
# keeps track of what has been drawn for mini wins
miniGUI = [[None for i in range(myGame.dim)] for j in range(myGame.dim)]
# to help display what is the current board for the current player to play in
cur = (-1, -1)

# cur move
drawBoard(window, 310, 80, 390, 160)
# keeps track of the text object
curGrid = Text(Point(350, 120), 'Cur')
# title
curTitle = Text(Point(350, 70), 'Cur Grid')
curTitle.draw(window)

# miniWins board
drawBoard(window, 310, 200, 390, 280)
title2 = Text(Point(350, 190), 'Mini Wins')
title2.draw(window)


while(myGame.getMoves() and not myGame.isEnd()):
	# human player
	if count % 2 == 0:
		getButtonClick(window)
		action = findMove()
		# until only one legal move is chosen
		while(action not in myGame.validMoves):
			print "Fix Board"
			getButtonClick(window)
			action = findMove()
		myGame.move(action)
		t = Text(Point(dist*action[0] + dist + (action[0]/3)*dist + 5*(action[0]%3), dist*action[1] + dist + (action[1]/3)*dist + 5*(action[1]%3)), 'x')
		t.draw(window)
		cells[action[0]][action[1]].undraw()
		cells[action[0]][action[1]] = None
		cur = (action[0] % 3, action[1] % 3)
	# minimax agent
	else:
		action = agent.getAction(myGame)
		myGame.move(action)
		t = Text(Point(dist*action[0] + dist + (action[0]/3)*dist + 5*(action[0]%3), dist*action[1] + dist + (action[1]/3)*dist + 5*(action[1]%3)), 'o')
		t.draw(window)
		cells[action[0]][action[1]].undraw()
		cells[action[0]][action[1]] = None
		cur = (action[0] % 3, action[1] % 3)
	# update the graphical miniWins
	for r in range(myGame.dim):
		for c in range(myGame.dim):
			# a new mini win just occured
			if miniGUI[r][c] == None and myGame.miniWins[r][c] != 0:
				win = ''
				if myGame.miniWins[r][c] == 1:
					win = 'x'
				else:
					win = 'o'
				t = Text(Point(dist*2 + 5 + r*rectDist + space*(r%3), dist*2 + c*rectDist + space*(c%3)), win)
				t.setSize(36)
				t.draw(window)
				miniGUI[r][c] = t
				# update the mini win grid on the GUI
				t2 = Text(Point(310 + r*80/3.0 + 15, 200 + c*80/3.0 + 15), win)
				t2.draw(window)
	# update the cur grid on the GUI
	curGrid.undraw()
	curGrid = Text(Point(310 + cur[0]*80/3.0 + 15, 80 + cur[1]*80/3.0 + 15), 'Cur')
	curGrid.draw(window)
	count += 1
print 'Winner: ', myGame.getWinner()


# display winner
winnerText = 'Winner: '
if myGame.getWinner() == 1:
	winnerText += 'X'
elif myGame.getWinner() == -1:
	winnerText += 'O'
else:
	winnerText = 'It\'s a tie!'
winner = Text(Point(175, 350), winnerText)
winner.setSize(36)
winner.draw(window)

# click button to end
getButtonClick(window)
window.close()