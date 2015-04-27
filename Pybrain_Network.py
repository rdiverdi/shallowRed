#This file contains everyhting I'm doing with pybrain, from datasets to the network itself

import pybrain
from pybrain.structure import LinearLayer, SigmoidLayer, FullConnection, FeedForwardNetwork

def create_network():
	network = FeedForwardNetwork()

	#Creating an input layer equal to 12 chessboards: 1 for each type of piece
	inlayer = LinearLayer(768)
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
	dataset = SupervisedDataSet(768, 128)
	for board, move_dict in board_data:
		pass

def create_board_input(board):
	'''Takes in the board part of the FEN string, outputs representative tuple'''
	#Tuple structure: Pawns, knights, bishops, rooks, queens, kings, oponents pieces

	output = [0 for i i(rows):n xrange(768)]
	index_dict = ['P':0, 'N':64, 'B':128, 'R':192, 'Q':256, 'K':320, 'p':384, 'n':448, 'b':512, 'r': 576, 'q':640, 'k':704]

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
	return move_list[0]/float(sum(move_list))

def loss_rate(move_list):
	return move_list[1]/float(sum(move_list))

def draw_rate(move_list):
	return move_list[2]/float(sum(move_list))

######################################
######################################

if __name__ == '__main__':
	network = create_network()
	print network


