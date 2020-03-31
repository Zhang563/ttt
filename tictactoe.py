import random, copy
import numpy as np

# Player -1 is o, +1 is x
class Game:
	def __init__(self, dim=3):
		self.dim = dim
		self.board = np.zeros((self.dim**2, self.dim**2))
		self.miniWins = np.zeros((self.dim, self.dim))
		self.currPlayer = -1 + 2*random.randint(0,1)
		self.validMoves = [(x,y) for x in range(self.dim*self.dim) for y in range(self.dim*self.dim)]
		self.numMoves = 0
		self.winner = 0

	def getMoves(self):
		return self.validMoves

	def getNumMoves(self):
		return self.numMoves

	def getRandomMove(self):
		return random.choice(self.validMoves)

	def getCurrPlayer(self):
		return self.currPlayer

	def getMiniWins(self):
		return self.miniWins

	def getBoard(self):
		return self.board

	def isEnd(self):
		return self.winner != 0 or not self.validMoves

	def getWinner(self):
		return self.winner

	def generateSuccessor(self, action):
		newGame = copy.deepcopy(self)
		newGame.move(action)
		return newGame

	# Option = 1: 9x9 board
	# Option = 2: self.dimxself.dim board of mini wins
	def printBoard(self, option=1):
		board = self.board if option == 1 else self.miniWins
		for i in range(len(board)):
			row = board[i]
			strrow = []
			for player in row:
				if player == -1:
					strrow.append('o')
				elif player == 1:
					strrow.append('x')
				else:
					strrow.append('_')
			strrow = ' '.join(strrow)
			strrow2 = ''
			for j in range(self.dim):
				strrow2 = strrow2 + strrow[2*self.dim*j : 2*self.dim*(j+1)] + ' '
			print(strrow2)
			if (i + 1) % self.dim == 0:
				print

	# Have current player move to position pos specified by a pair (row, col)
	def move(self,pos):
		if not pos in self.validMoves:
			raise Exception("Invalid Move")
		self.board[pos[0]][pos[1]] = self.currPlayer
		self.updateMiniWinners(pos)
		self.updateWinner()
		self.updateValidMoves(pos)
		self.currPlayer = -self.currPlayer
		self.numMoves += 1

	# Utility method called by the move method after each move to 
	# set the valid moves for the next player
	def updateValidMoves(self,pos):
		self.validMoves = []

		# First look at all the squares in the current mini-board
		r0 = pos[0] % self.dim
		c0 = pos[1] % self.dim
		for dr in range(self.dim):
			for dc in range(self.dim):
				r = self.dim*r0 + dr
				c = self.dim*c0 + dc
				if self.board[r][c] == 0:
					self.validMoves.append((r,c))

		# If all squares in the current mini-board are taken, pick any open grid
		# on the screen
		if self.validMoves == []:
			for r in range(self.dim**2):
				for c in range(self.dim**2):
					if self.board[r][c] == 0:
						self.validMoves.append((r,c))

	# Utility method called by move method
	# Updates the grid specifying which mini-boards have been won by which players
	def updateMiniWinners(self,pos):
		r0 = pos[0]//self.dim
		c0 = pos[1]//self.dim

		row = r0 * self.dim
		col = c0 * self.dim

		miniBoard = self.board[row : row + self.dim, col : col + self.dim]
		if self.miniWins[r0][c0] == 0 and self.hasWinningPattern(miniBoard):
			self.miniWins[r0][c0] = self.currPlayer

	# Utility method called by move method
	# Updates the winner by examining the miniWins board
	def updateWinner(self):
		if self.winner == 0 and self.hasWinningPattern(self.miniWins):
			self.winner = self.currPlayer

	# Utiliy method called by updateMiniWinners and updateWinner
	# Checks a self.dim by self.dim board to find a winning pattern
	def hasWinningPattern(self, board):
		# Check row totals
		for dr in range(self.dim):
			rowTotal = sum(board[dr, i] for i in range(self.dim))
			if abs(rowTotal) == self.dim:
				return True
				
		# Check column totals
		for dc in range(self.dim):
			colTotal = sum(board[i, dc] for i in range(self.dim))
			if abs(colTotal) == self.dim:
				return True

		# Check diagonal totals
		diagTotal = sum(board[i, i] for i in range(self.dim))
		if abs(diagTotal) == self.dim:
			return True
		
		diagTotal = sum(board[self.dim - 1 - i, i] for i in range(self.dim))
		if abs(diagTotal) == self.dim:
			return True
		return False

