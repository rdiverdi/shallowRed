import time
import random
import copy
import ChessBoard

piece_values = {'P':1, 'N':3, 'B':3, 'R':5, 'Q':9, 'K':102, 'p':-1, 'n':-3, 'b':-3, 'r':-5, 'q':-9, 'k':-102}

def evaluate_board(chessboard, white, piece_values = piece_values):
	""" Takes in a board object, as well as
		a boolean indicating whether or not white is evaluating.
		current algorithms sums own pieces and subtracts white's pieces
		Optionally, you can specify the value of the pieces.

		>>> chessboard = ChessBoard.ChessBoard()
		>>> evaluate_board(chessboard, True)
		0
	"""

	board = chessboard.getBoard()
	value = 0
	for row in board:
		for char in row:
			if char in piece_values:
				value += piece_values[char]

	if white:
		return value
	else:
		return -value

def get_all_valid_moves(chessboard):
	moves = []
	for i in xrange(8):
		for j in xrange(8):
			moves += [((i,j), move) for move in chessboard.getValidMoves((i,j))]
	return moves


def find_move_index(numbers):
	"""Takes in a list of numbers, and retuns the indexes of the maxes."""
	best = [0]
	for i in range(len(numbers)):
		if numbers[i] > numbers[best[0]]:
			best = [i]
		elif numbers[i] == numbers[best[0]]:
			best.append(i)
	return best


class BoardEvaluation(object):

	def __init__(self, chessboard, white, BoardEvaluator):
		"""	chessboard: an instance of ChessBoard
			white: whether the 
		"""
		self.chessboard = copy.deepcopy(chessboard)
		self.white = white
		self.current_move = random.choice(get_all_valid_moves(chessboard))
		self.branches = [Branch(move) for move in get_all_valid_moves(self.chessboard)]
		self.BoardEvaluator = BoardEvaluator

	def evaluate(self, max_time):
		level = 0
		max_time = time.time() + max_time
		while time.time() < max_time: #Doesn't account for timeout occuring durring the loop. Will fix soon.
			if self.branches:
				worst_value = self.branches[0].evaluate(self.chessboard, False, level, self.BoardEvaluator, self.white, max_time)
				evaluations = [worst_value]
				counter = 1
				while time.time() < max_time and counter < len(self.branches):
					evaluations.append(self.branches[counter].evaluate(self.chessboard, False, level, self.BoardEvaluator, self.white, max_time, worst_value))
					if evaluations[counter] < worst_value:
						worst_value = evaluations[counter]
					counter += 1
				if evaluations == len(self.branches): #If this layer's calculations are done, return the best move.
					self.current_move = self.branches[random.choice(find_move_index(evaluations))].move #Fine the actual move for the best branch
			else:
				return None #Might want to fix this. I can't imagine it ever returning, for what I'm doing now, but it could probably break something 
			level += 1
		return self.current_move


class Branch(object):

	def __init__(self, move):
		self.move = move
		self.branches = []
		self.is_setup = False

	def setup(self, chessboard):
		''' Does all of the work that makes the process of making a possible move slow
			It takes in the chessborad that it is supposed to be modifying.

			>>> chessboard = ChessBoard.ChessBoard()
			>>> chessboard.setFEN("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
			>>> a_branch = Branch(((0,6),(0,5)))
			>>> print a_branch.is_setup
			False
			>>> a_branch.setup(chessboard)
			>>> print a_branch.is_setup
			True
			>>> a_branch.evaluate(chessboard, True, 0, evaluate_board, True, time.time() + 30)
			0
			>>> '''
		self.chessboard = copy.deepcopy(chessboard) 
		self.chessboard.addMove(self.move[0], self.move[1])
		self.branches = [Branch(move) for move in get_all_valid_moves(self.chessboard)]
		self.is_setup = True

	def evaluate(self, chessboard, maxplayer, level, BoardEvaluator, white, max_time, worst_value = None):
		''' Evaluates current board value recursively.
		'''
		if not self.is_setup:
			self.setup(chessboard)
		if level == 0:
			return BoardEvaluator(self.chessboard, white)
		if not self.branches:
			#I'm pretty sure this bit will result in the program being absolutly, completely, unwilling to win.
			#We should fix that. But right now I just want to see if it is willing to play.
			return BoardEvaluator(self.chessboard, white)
		if maxplayer:
			counter = 1
			evaluations = [self.branches[0].evaluate(self.chessboard, not maxplayer, level-1, BoardEvaluator, white, max_time, worst_value)]
			while time.time() < max_time and counter < len(self.branches):
				evaluations.append(self.branches[counter].evaluate(self.chessboard, not maxplayer, level-1, BoardEvaluator, white, max_time, worst_value))
				counter += 1
			return max(evaluations)
		else:
			if not worst_value: #TODO: Make this bit less stupid. It doesn't do time evaluation, and won't break anything, but just doesn't seem right
				return min([self.branches[i].evaluate(self.chessboard, not maxplayer, level-1, BoardEvaluator, white, max_time) for i in xrange(len(self.branches))])
			current_value = self.branches[0].evaluate(self.chessboard, not maxplayer, level-1, BoardEvaluator, white, max_time, worst_value)
			counter = 0
			while time.time() < max_time and current_value>worst_value and counter<len(self.branches):
				current_value = self.branches[counter].evaluate(self.chessboard, not maxplayer, level-1, BoardEvaluator, white, max_time, worst_value)
				counter += 1
			return current_value

if __name__ == '__main__':
    import doctest
    doctest.testmod()






