"""Parses the .pgn files that contain the chess games we want to look at, and process into a dictionary."""

import pgn
import sys
import pickle
import ChessBoard
from os.path import exists

#get the chess game information
f = open(sys.argv[1])
pgn_text = f.read()
f.close()

games = pgn.loads(pgn_text)

def who_won(game):
	"""Checks to see who won the game, returns the answer"""
	if game.moves[-1] == '1-0':
		return 'w'
	elif game.moves[-1] == '0-1':
		return 'b'
	else:
		return False

def did_I_win(win, white):
	"""Takes in a win variable, and whether or not the player was white,
	   and tells whether it was a win, loss, or draw for that player,
	   in the form of a (win,los,draw) tuple"""
	if white:
		if win == 'w':
			return [1,0,0]
		elif win == 'b':
			return [0,1,0]
		else:
			return [0,0,1]
	else:
		if win == 'w':
			return [1,0,0]
		elif win == 'b':
			return [0,1,0]
		else:
			return [0,0,1]

boards = {}
for game in games:
	'''Stores in a dicionary:
		key: (board state in FEN notation, white's turn boolean) as a tuple
		value: dictionary of moves

		in the dictionary of moves:
		key: the move tuple
		value: [wins, losses, draws] by number'''
	chessboard = ChessBoard.ChessBoard()
	win = who_won(game)
	white = True

	for move in game.moves[0:len(game.moves)-2]:
		FEN = chessboard.getFEN().split() #Gets the FEN of the chessboard, and turns it into a list so we can just get board position
		board = (FEN[0], white) #describes the current board state
		chessboard.addTextMove(move) #lets me get the previous move in a sensable notation later, and sets up for next move evaluation
		if board in boards:
			move = chessboard.getLastMove() #Move, in ChessBoard's internal notation, which is easy to think in
			result = did_I_win(win, white) #Result in list form, showing whether or not this particular choice led to a win
			if move in boards[board]: 
				#Updates the [win, loss, draw] results of a move for a given board
				boards[board][move][0] += result[0]
				boards[board][move][1] += result[1]
				boards[board][move][2] += result[2]
			else:
				#Sets the [win, loss, draw] results of a board for the first time
				boards[board][move] = result
		else:
			#If this board hasn't occured before, create an entry and add this move/result pair to it.
			result = did_I_win(win, white)
			move_dict = {chessboard.getLastMove():result}
			boards[board] = move_dict

		white = not white

#open a file to store the data for later use
file_name = sys.argv[2]
data_file = open(file_name, "w")
pickle.dump(boards, data_file)