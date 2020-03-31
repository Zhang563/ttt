import tictactoe
import random

# This evaluation function takes up the number of mini wins of 'x' minus
# the number of mini wins of 'o'

class AlphaBetaAgent():
	def __init__(self, evalFn = None, depth = 3):
		self.index = 0
		self.depth = depth

	def evaluationFunction(self, gameState):
		return float('inf')*gameState.getWinner() + sum(sum(wins) for wins in gameState.getMiniWins())


	def getAction(self, gameState):
		"""
		Returns the minimax action using self.depth and self.evaluationFunction
		"""

		# Return a random move for first five moves
		if gameState.getNumMoves() < 10:
			return gameState.getRandomMove()

		def recurse(gameState, player, depth, alpha, beta):
			if gameState.isEnd() or depth == 0:
				return (self.evaluationFunction(gameState), (-1,-1))

			moves = gameState.getMoves()
			if player == 1:
				ans = (-float('Inf'),(-1,-1))
				for action in moves:
					ans = max(ans, (recurse(gameState.generateSuccessor(action), 
							-player, depth - 1, alpha, beta)[0], action))
					alpha = max(alpha, ans)
					if alpha >= beta:
						break
				return alpha
			else:
				ans = (float('Inf'),(-1,-1))
				for action in moves:
					ans = min(ans, (recurse(gameState.generateSuccessor(action), 
							-player, depth - 1, alpha, beta)[0], action))
					beta = min(beta, ans)
					if alpha >= beta:
						break
				return beta
		alph0 = (-float('Inf'), (-1,-1))
		beta0 = (+float('Inf'), (-1,-1))
		utility, action = recurse(gameState, gameState.getCurrPlayer(), 2*self.depth, alph0, beta0)
		if action != (-1,-1):
			return action
		else:
			return gameState.getRandomMove()
