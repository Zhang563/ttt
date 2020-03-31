import random, copy, math, collections
import tictactoe

class Node:
	def __init__(self, move=None, parent=None, state=tictactoe.Game(), agent=None):
		self.move = move # the move that got us to this node
		self.parentNode = parent
		self.childNodes = []
		self.wins = 0
		self.visits = 0
		self.state = state
		self.agent = agent
		self.untriedMoves = copy.deepcopy(state.getMoves())

	def __repr__(self):
		return "[M:" + str(self.move) + "W/V:" + str(self.wins) + "/" + str(self.visits) + "]"

	def UCTSelectChild(self):
		return sorted(self.childNodes, key = lambda c: c.wins/c.visits + math.sqrt(2*math.log(self.visits)/c.visits))[-1]
	
	# Remove m from untriedMoves and return added child node
	def AddChild(self, m):
		newState = self.state.generateSuccessor(m)
		n = Node(move=m, parent=self, state=newState, agent=self.agent)
		self.untriedMoves.remove(m)
		self.childNodes.append(n)
		return n

	def Update(self, result):
		self.visits += 1
		self.wins += result

	def orderMoves(self, moves):
		valsAndMoves = []
		sortedMoves = []
		moveDict = collections.defaultdict(float)
		for move in moves:
			newState = self.state.generateSuccessor(move)
			val = 1 - self.agent.getVal(newState) if self.agent != None else 1
			moveDict[move] = val
		return moveDict

	def childrenToString(self):
		s = ""
		for c in self.childNodes:
			s += str(c) + "\n"
		return s

class MCTSagent:
	def __init__(self, itermax=100, agent=None):
		self.itermax = itermax
		self.agent = agent
		self.epsilon = 0.8

	def getAction(self, game):
		rootnode = Node(state=game, agent=self.agent)

		for i in range(self.itermax):
			node = rootnode
			state = copy.deepcopy(game)

			# Select
			while node.untriedMoves == [] and node.childNodes != []:
				node = node.UCTSelectChild()
				state.move(node.move)

			# Expand
			if node.untriedMoves != []:
				m = random.choice(node.untriedMoves)
				state.move(m)
				node = node.AddChild(m)

			# Rollout
			while not state.isEnd():
				if self.agent == None or random.random() < self.epsilon:
					state.move(state.getRandomMove())
				else:
					state.move(self.agent.getAction(state))
			if state.getWinner() == game.getCurrPlayer():
				result = 1
			elif state.getWinner() == 0:
				result = 0.5
			else:
				result = 0

			# Backpropogate
			while node != None:
				node.Update(result)
				node = node.parentNode
		return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move

