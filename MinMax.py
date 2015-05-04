import time
import random
import copy
import ChessBoard
#TODO: Delete all of the TODOS. They weren't important anyways.

piece_values = {'P':1, 'N':3, 'B':3, 'R':5, 'Q':9, 'K':102, 'p':-1, 'n':-3, 'b':-3, 'r':-5, 'q':-9, 'k':-102}

def evaluate_board(chessboard, white, piece_values = piece_values):
	""" Takes in a board object, as well as
		a boolean indicating whether or not white is evaluating.
		current algorithms sums own pieces and subtracts white's pieces
		Optionally, you can specify the value of the pieces.

		>>> chessboard = ChessBoard.ChessBoard()
		>>> evaluate_board(chessboard, True)
		0
		>>> chessboard.setFEN("8/8/8/8/8/8/8/7P w KQkq - 0 1")
		>>> evaluate_board(chessboard, True)
		1
	"""

	board = chessboard.getBoard()
	value = 0
	for row in board:
		for char in row:
			if char in piece_values:
				value += piece_values[char]

	if white: #The black evaluation should be symetrical, but in its own favor. I think.
		return value
	else:
		return -value

def get_all_valid_moves(chessboard):
	"""Returns a list of all possible moves, using the built in function
		for getting moves on a square

		>>> chessboard = ChessBoard.ChessBoard()
		>>> chessboard.setFEN("8/8/8/8/8/8/8/7P w KQkq - 0 1")
		>>> get_all_valid_moves(chessboard)
		[((7, 7), (7, 6))]
	"""
	moves = []
	for i in xrange(8):
		for j in xrange(8):
			moves += [((i,j), move) for move in chessboard.getValidMoves((i,j))]
	return moves


def find_move_index(numbers):
	"""Takes in a list of numbers, and retuns the indexes of the maxes.

		>>> find_move_index([1, 2, 2, 3, 2, 1])
		[3]
		>>> find_move_index([1, 2, 2, 1, 2, 1])
		[1, 2, 4]
	"""
	best = [0]
	for i in range(len(numbers)):
		if numbers[i] > numbers[best[0]]:
			best = [i]
		elif numbers[i] == numbers[best[0]]:
			best.append(i)
	return best


class BoardEvaluation(object):

	def __init__(self, chessboard, white, BoardEvaluator = evaluate_board):
		"""	chessboard: an instance of ChessBoard
			white: whether it is white's move (boolean)
			BoardEvaluator: board evaluation function
		"""
		self.chessboard = copy.deepcopy(chessboard)
		self.white = white
		self.current_move = random.choice(get_all_valid_moves(chessboard))
		self.branches = [Branch(move) for move in get_all_valid_moves(self.chessboard)]
		self.BoardEvaluator = BoardEvaluator

	def evaluate(self, max_time):
		level = 0
		max_time = time.time() + max_time
		while time.time() < max_time:
			if self.branches:
				best_value = self.branches[0].evaluate(self.chessboard, False, level, self.BoardEvaluator, self.white, max_time)
				#print best_value
				evaluations = [best_value]
				counter = 1
				while time.time() < max_time and counter < len(self.branches):
					evaluations.append(self.branches[counter].evaluate(self.chessboard, False, level, self.BoardEvaluator, self.white, max_time, best_value))
					#print evaluations[-1]
					if evaluations[counter] > best_value:
						best_value = evaluations[counter]
						#print 'change best', best_value
					counter += 1
				if len(evaluations) == len(self.branches): #If this layer's calculations are done, return the best move.
					#print 'banana'
					self.current_move = self.branches[random.choice(find_move_index(evaluations))].move #Fine the actual move for the best branch
			else:
				return None #Might want to fix this. I can't imagine it ever returning, for what I'm doing now, but it could probably break something
			level += 1
		print 'Level reached: ' + str(level)
		return self.current_move

	def eval_by_dict(self, board_dict):
		""" Takes in a dictionary of boards,
			searches for the best move to make at a specific board position,
			and outputs that move in the form of the resultant board.
			Uses a ratio of possible wins and possible losses of each move,
			ignoring draws and giving priority to high ratios with greater overall wins.
		"""
		value = None
		best_move = ()
		board = self.chessboard.getFEN().split()[0]
		if board in board_dict:
			for moves in board_dict[board]:
				if board_dict[board][moves][1] == 0: #if move hasn't lost
					if board_dict[board][moves][0] != 0: #if move has won but never lost
						value = board_dict[board][moves][0]*1000000000
						best_move = moves
					elif value == None: #if move has only drawn and best_move hasn't been set
						value = 0.
						best_move = moves
				else:
					new_val = float(board_dict[board][moves][0]/board_dict[board][moves][1])
					if new_val > value: #if this move is better than existing best
						value = new_val
						best_move = moves
					elif new_val==value) and board_dict[board][moves][0]>board_dict[board][best_move][0]:
						#if this value = current max value AND more overall wins
						value = new_val
						best_move = moves
		return best_move


class Branch(object):

	def __init__(self, move):
		self.move = move
		self.branches = []
		self.is_setup = False

	def setup(self, chessboard):
		''' Makes a move on a chessboard, then generates all possible responses to that move
			It takes in the chessboard that it is supposed to be modifying.

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
			>>>
		'''
		self.chessboard = copy.deepcopy(chessboard)
		self.chessboard.addMove(self.move[0], self.move[1])
		self.branches = [Branch(move) for move in get_all_valid_moves(self.chessboard)]
		self.is_setup = True #Lets the branch exist with minimal processing, for alpha-beta pruning

	def evaluate(self, chessboard, maxplayer, level, BoardEvaluator, white, max_time, best_value = None):
		''' Evaluates current board value recursively.

			>>> chessboard = ChessBoard.ChessBoard()
			>>> chessboard.setFEN("8/8/6p1/6B1/8/8/4k1K1/1Q1qb3 w KQkq - 1 2")
			>>> a_branch = Branch(((1, 7), (4, 4)))
			>>> a_branch.setup(chessboard)
			>>> a_branch.evaluate(chessboard, True, 0, evaluate_board, True, time.time() + 30)
			inf
		'''
		if not self.is_setup:
			self.setup(chessboard) #Creates a new chessboard object, makes a move on it, and finds all of the possible moves
		if level == 0:
			return self.evaluate_board_state(white, level, BoardEvaluator)
		if not self.branches:
			return self.evaluate_board_state(white, level, BoardEvaluator)
		if maxplayer: #Looks for the largest possible value, because it needs to find tohe biggest payoff
			return self.max_evaluation(level, BoardEvaluator, white, max_time, best_value)
		else: #Looks for a value worse than the current best case scenario. Returns the first value that fits the criteria
			return self.min_evaluation(level, BoardEvaluator, white, max_time, best_value)

	def max_evaluation(self, level, BoardEvaluator, white, max_time, best_value):
		"""
		"""
		counter = 1
		evaluations = [self.branches[0].evaluate(self.chessboard, False, level-1, BoardEvaluator, white, max_time, best_value)]
		while time.time() < max_time and counter < len(self.branches):
			evaluations.append(self.branches[counter].evaluate(self.chessboard,
								False, #sets next evaluation to be minimizing
								level-1, #decrements the level tracker, to end recursion
								BoardEvaluator,
								white,
								max_time, #conotinues time dependency
								best_value))
			counter += 1
		val = max(evaluations)
		return val

	def min_evaluation(self, level, BoardEvaluator, white, max_time, best_value = None):
		"""
		"""
		if not best_value: #TODO: Make this bit less stupid. It doesn't do time evaluation, and won't break anything, but just doesn't seem right
				return min([self.branches[i].evaluate(self.chessboard, True, level-1, BoardEvaluator, white, max_time) for i in xrange(len(self.branches))])
		else:
			current_value = self.branches[0].evaluate(self.chessboard, True, level-1, BoardEvaluator, white, max_time, best_value)
			counter = 0
			while time.time() < max_time and current_value>=best_value and counter<len(self.branches):
				value = self.branches[counter].evaluate(self.chessboard, True, level-1, BoardEvaluator, white, max_time, best_value)
				if value < current_value:
					current_value = value
				counter += 1
			return current_value

	def evaluate_board_state(self, white, level, BoardEvaluator):
		""" Allows evaluation while checking for checkmates.
			This takes in  which player you are, how deep in the recursion
			(for the sake of finding faster checkmates), and the
			evaluation function. It outputs a board score
		"""
		if self.chessboard.getGameResult() == self.chessboard.WHITE_WIN: #1 means that white has won
			if white:
				return 200 + 200*level
			else:
				return - 200 - 200*level
		elif self.chessboard.getGameResult() == self.chessboard.BLACK_WIN: #2 means that black has won
			if white:
				return - 200 - 200*level
			else:
				return 200 + 200*level
		else:
			return BoardEvaluator(self.chessboard, white) #TODO: better draw handling


if __name__ == '__main__':
    import doctest
    doctest.testmod()






