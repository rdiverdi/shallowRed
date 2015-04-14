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
		self.weights = [init_weights((sizes[i], sizes[i+1])) for i in xrange(1,len(sizes)-1)]

	def model(self, X, p_drop_input, p_drop_hidden):
		""" X is the set of inputs, which must be the same size as the first number in self.sizes
			Weights are included in self, and are updated as the program goes. 
			p_drop input is the probability of droping a node in the input layer, while p_drop_hidden is
			the probability of a node being dropped in the hiddend layers
		"""
	    X = dropout(X, p_drop_input)
	    h = rectify(T.dot(X, w_h))

	    h = dropout(h, p_drop_hidden)
	    h2 = rectify(T.dot(h, w_h2))

	    h2 = dropout(h2, p_drop_hidden)
	    py_x = softmax(T.dot(h2, w_o))
	    return h, h2, py_x
		


def floatX(X):
    return np.asarray(X, dtype=theano.config.floatX)

def init_weights(shape):
    return theano.shared(floatX(np.random.randn(*shape) * 0.01))

def rectify(X):
    return T.maximum(X, 0.)

def softmax(X):
    e_x = T.exp(X - X.max(axis=1).dimshuffle(0, 'x'))
    return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')

def RMSprop(cost, params, lr=0.001, rho=0.9, epsilon=1e-6):
    grads = T.grad(cost=cost, wrt=params)
    updates = []
    for p, g in zip(params, grads):
        acc = theano.shared(p.get_value() * 0.)
        acc_new = rho * acc + (1 - rho) * g ** 2
        gradient_scaling = T.sqrt(acc_new + epsilon)
        g = g / gradient_scaling
        updates.append((acc, acc_new))
        updates.append((p, p - lr * g))
    return updates

def dropout(X, p=0.):
    if p > 0:
        retain_prob = 1 - p
        X *= srng.binomial(X.shape, p=retain_prob, dtype=theano.config.floatX)
        X /= retain_prob
    return X