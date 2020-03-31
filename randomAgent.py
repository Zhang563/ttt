import tictactoe

class RandomAgent():
	def getAction(self, gameState):
		return gameState.getRandomMove()