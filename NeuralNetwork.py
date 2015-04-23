"""Building code for an arbitrarily sized neural network, using the same functions as Alec's Modern Net"""
import theano
from theano import tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import numpy as np
from load import mnist

srng = RandomStreams()


class NeuralNetwork(object):
	"""A Neural Network of arbitry size, with evaluation functions"""
	def __init__(self, sizes):
		""" Takes in a list, corresponding to the number of nodes in each layer. The input and output
			layers must be included in this list, leaving a minimum length of 3 (input, hidden layer, output)"""
		self.num_layers = len(sizes)
		self.sizes = sizes
		self.biases = 
		self.weights = [init_weights((sizes[i], sizes[i+1])) for i in xrange(1,len(sizes)-1)]

	def model(self, X, p_drop_input, p_drop_hidden):
		""" X is the set of inputs, which must be the same size as the first number in self.sizes
			Weights are included in self, and are updated as the program goes.

			returns: 
		"""
		
	def feedforward(self, a):
		""" Returns the output of the network, if 'a' is
			a vector of inputs
		"""
		for b, w in zip(self.biases, self.weights):
			a = sigmoid_vec(np.dot(w, a) + b)
		return a