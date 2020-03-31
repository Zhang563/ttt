import numpy as np
from keras.models import Sequential, Model
from keras import layers
from keras import optimizers
import collections, random
import tictactoe

class DQNagent:
	def __init__(self, dim=3):
		self.state_size = (dim**2, dim**2, 4)
		self.memory = collections.deque(maxlen=2000)
		self.gamma = 0.95    # discount rate
		self.epsilon = 1.0  # exploration rate
		self.epsilon_min = 0.01
		self.epsilon_decay = 0.995
		self.learning_rate = 0.0001
		self.model = self._build_model()
		self.history = None

	def _build_model(self):
		# Neural Net for Deep-Q learning Model
		board_input = layers.Input(shape=self.state_size, name='board')

		board_cnn = layers.Conv2D(64, (3,3), activation='relu', strides=(3,3)) (board_input)
		board_cnn = layers.Dropout(0.2)(board_cnn)

		dense_0 = layers.Flatten()(board_cnn)

		dense_1 = layers.Dense(16, activation='relu')(dense_0)
		dense_1 = layers.Dropout(0.2)(dense_1)

		probability = layers.Dense(1, activation='tanh')(dense_1)
		model = Model(board_input, probability)
		model.compile(loss='mean_squared_error', optimizer='rmsprop')
		model.summary()
		return model

	def remember(self, state, next_state, winner):
		self.memory.append((state, next_state, winner))

	def extractState(self, game):
		state = np.zeros((1, self.state_size[0], self.state_size[1], self.state_size[2]))
		state[0,:,:,0] = (game.getBoard() == 1)
		state[0,:,:,1] = (game.getBoard() == -1)
		state[0,:,:,2] = (game.getCurrPlayer() == 1)
		for move in game.getMoves():
			state[0,move[0],move[1],3] = 1
		return state

	def getAction(self, game):
		moves = game.getMoves()
		if np.random.rand() <= self.epsilon:
			i = random.randint(0,len(moves)-1)
			return moves[i]
		q = []
		for action in moves:
			newState = game.generateSuccessor(action)
			q.append((-self.getVal(newState), action))

		return max(q)[1]

	def getVal(self, game):
		return self.model.predict(self.extractState(game))[0][0] * game.getCurrPlayer()

	def getPolicy(self, game):
		moves = game.getMoves()
		vals = []
		sumVals = 0
		for action in moves:
			newState = game.generateSuccessor(action)
			val = 1 - self.getVal(newState)
			vals.append(val)
			sumVals += val
		policy = collections.defaultdict(float)
		for i, val in enumerate(vals):
			policy[moves[i]] = val/sumVals
		return policy

	def replay(self, batch_size, verbose=False):
		minibatch = random.sample(self.memory, batch_size)
		states = np.zeros((batch_size, self.state_size[0], self.state_size[1], self.state_size[2]))
		targets = np.zeros((batch_size, 1))

		for i, (state, next_state, weight) in enumerate(minibatch):
			states[i] = state
			targets[i] = [weight]
		
		self.history = self.model.fit(states, targets, epochs=1, verbose=0)

		if verbose:
			print('Loss:', self.history.history['loss'][0])
			print(targets[5], self.model.predict([[states[5]]]))

		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay

