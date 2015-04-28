#This file contains everyhting I'm doing with pybrain, from datasets to the network itself

import pybrain
from pybrain.structure import LinearLayer, SigmoidLayer, FullConnection, FeedForwardNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
import pickle
import random

def create_network():
	network = FeedForwardNetwork()

	#Creating an input layer equal to 12 chessboards: 1 board for each type of piece
	inlayer = LinearLayer(768) #12 boards = 12*64 = 768 nodes
	hidden1 = SigmoidLayer(2048)
	hidden2 = SigmoidLayer(2048)
	hidden3 = SigmoidLayer(2048)
	outlayer = LinearLayer(128)

	#Telling the network what the layers are
	network.addInputModule(inlayer)
	network.addModule(hidden1)
	network.addModule(hidden2)
	network.addModule(hidden3)
	network.addOutputModule(outlayer)

	#Connecting the layers
	in_to_hidden = FullConnection(inlayer, hidden1)
	connect1 = FullConnection(hidden1, hidden2)
	connect2 = FullConnection(hidden2, hidden3)
	hidden_to_out = FullConnection(hidden3, outlayer)

	#Adding the networks
	network.addConnection(in_to_hidden)
	network.addConnection(connect1)
	network.addConnection(connect2)
	network.addConnection(hidden_to_out)

	#Initializing the network
	network.sortModules()

	return network

######################################
######## Dictionary Processing #######
######################################
def dictionary_to_dataset(board_data):
	dataset = SupervisedDataSet(12*64, 2*64) #12 board input, 2 board output (12 or 2 *64)
	for board, move_dict in board_data:
		dataset.addSample(create_board_input(board),create_board_result(move_dict))
	return dataset

def dictionary_stripper(filename, White = True):
	""" This function returns only the boards for one side from one
		of our weird files.
	"""
	f = open(filename, 'r')
	dictionary = pickle.load(f)
	f.close()

	newDict = {}
	for boardstate in dictionary:
		if boardstate[1] and White:
			newDict[boardstate[0]] = dictionary[boardstate]
		elif not boardstate[1] and not White:
			newDict[boardstate[0]] = dictionary[boardstate]

	return newDict

def create_board_result(move_dict):
	""" Takes in a move dictionary from a board, and returns a tuple describing the propper output.

		Tuple structure: two boards, each represented by a portion of the list with 64 entries
		Each board should have one position with a 1 in it 
		(the position a piece comes from, the position it goes to)"""
	output = [0 for i in xrange(2*64)] #From chessboard and to chessboard (64 inputs each)
	move = best_move(move_dict)
	from_square = move[0]
	to_quare = move[1]

	from_index = from_square[0]*8 + from_square[1]
	output[from_index] = 1
	to_index = 64 + to_square[0]*8 + to_square[1] #64 is to get to the next list
	output[to_index] = 1

	return tuple(output)


def create_board_input(board):
	""" Takes in the board part of the FEN string, outputs representative tuple

		Tuple structure: Pawns, knights, bishops, rooks, queens, kings, oponents pieces"""

	output = [0 for i in xrange(12*64)] #12 chessboards in a row, in list form
	index_dict = {'P':0, 'N':64, 'B':2*64, 'R':3*64, 'Q':4*64, 'K':5*64, 'p':6*64, 'n':7*64, 'b':8*64, 'r': 9*64, 'q':10*64, 'k':11*64}

	rows = board.split("/")
	for index, row in enumerate(rows):
		newrow = ""
		for char in row:
			if char in '123456789':
				newrow += "."*int(char)
			else:
				newrow += char
		rows[index] = newrow

	for i, row in enumerate(rows):
		for j, entry in enumerate(row):
			if entry in index_dict:
				output[index_dict[entry] + i*8 + j] = 1
	return tuple(output)


def best_move(move_dict):
	""" Takes in a dictionary of moves:win/loss/draw rates, and returns a decent one
	"""
	best_move = None
	for move, value in move_dict:
		if not best_move:
			best_move = [move, value]

		if win_rate(value) > win_rate(best_move[1]):
			best_move = [move, value]
		elif win_rate(value) == win_rate(best_move[1]) and draw_rate(value) < draw_rate(best_move[1]):
			best_move = [move, value]

	return best_move

def win_rate(move_list):
	""" Takes in a list, [wins, losses, draws] and returns the percent of wins
	"""
	return move_list[0]/float(sum(move_list))

def loss_rate(move_list):
	""" Takes in a list, [wins, losses, draws] and returns the percent of losses
	"""
	return move_list[1]/float(sum(move_list))

def draw_rate(move_list):
	""" Takes in a list, [wins, losses, draws] and returns the percent of draws
	"""
	return move_list[2]/float(sum(move_list))

######################################
######################################

if __name__ == '__main__':
	print "Creating Network"
	network = create_network()
	print "Opening Data File"
	large_dict = dictionary_stripper("2000_data.txt")

	# print "Getting Keys"
	# keys = large_dict.keys()
	# newdict = {}
	# print "Sorting Dataset"
	# for i in xrange(20000):
	# 	key = keys[random.randint(len(keys))]
	# 	newdict[key] = large_dict[key]

	print "Training Dataset"
	dataset = dictionary_to_dataset(large_dict)
	trainer = BackpropTrainer(network, dataset)
	for i in xrange(500):
		result = trainer.train()
		print "Epoch %: %"%(str(i), result)

	f = open("Saved_Network.txt")
	pickle.dump(trainer, f)
	f.close()
