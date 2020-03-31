import tictactoe
import random
from minimax import AlphaBetaAgent
from mcts import MCTSagent
from DQNagent import DQNagent
from randomAgent import RandomAgent
from hybridAgent import HybridAgent
import time

agentNames = ['Random', 'Minimax', 'MCTS', 'DQN', 'Hybrid']
agents = [RandomAgent(),
		AlphaBetaAgent(depth=2), 
		MCTSagent(itermax=100), 
		DQNagent(),
		HybridAgent()]
agents[3].model.load_weights("dqnModel.h5")
agents[4].agent1 = agents[2]
agents[4].agent2 = agents[1]

f = open("results.txt", "w")

def simulateGames(agent1, agent2, n = 100):
	wins1 = 0
	wins2 = 0

	for i in range(n):
		myGame = tictactoe.Game()
		myGame.currPlayer = 1 # First player to move (count = 0) is agent 1
		while(myGame.getMoves() and not myGame.isEnd()):
			if myGame.getNumMoves() % 2 == 0:
				myGame.move(agent1.getAction(myGame))
			else:
				myGame.move(agent2.getAction(myGame))

		if myGame.getWinner() == 1:
			wins1 += 1
		elif myGame.getWinner() == -1:
			wins2 += 1

	print('Player 1 won {} games, player 2 won {} games, {} ties'.format(wins1, wins2, n-wins1-wins2))
	f.write('{},{},{}\n'.format(wins1, wins2, n-wins1-wins2))

def main():
	for i, agentName1 in enumerate(agentNames):
		for j, agentName2 in enumerate(agentNames):
			agent1 = agents[i]
			agent2 = agents[j]
			a = time.time()
			print('{} (Player 1) vs {} (Player 2)'.format(agentName1, agentName2))
			simulateGames(agent1, agent2)
			print('Runtime: {} seconds'.format(time.time() - a))
	f.close()

main()