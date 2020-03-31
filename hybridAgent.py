import tictactoe
from minimax import AlphaBetaAgent
from mcts import MCTSagent

class HybridAgent:
	def __init__(self):
		self.mcts = MCTSagent(itermax=15, agent=AlphaBetaAgent(depth=1))

	def getAction(self, gameState):
		return self.mcts.getAction(gameState)