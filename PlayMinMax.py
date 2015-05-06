"""I'm just testing things. This lets you play the basic chess algorithm that I made. You'll beat it. It's inevitable, really."""
import ChessBoard
import MinMax
import time
import pickle

def makeBoard():
	return ChessBoard.ChessBoard()

def AI_Move(chessboard, white, max_time, dictionary = None):
	evaluation = MinMax.BoardEvaluation(chessboard, white, MinMax.evaluate_board)
	curr_time = time.time()
	if dictionary:
		dictionary_move = evaluation.eval_by_dict(dictionary)
	else:
		dictionary_move = None

	if dictionary_move:
		print "Move found in dictionary."
		chessboard.addMove(dictionary_move[0], dictionary_move[1])
	else:
		AI_move = evaluation.evaluate(max_time)
		print "Turn calculation took: " + str(time.time() - curr_time) + " seconds"
		chessboard.addMove(AI_move[0], AI_move[1])
	chessboard.printBoard()

def playerMove(chessboard, move):
	thingie = chessboard.addTextMove(move)
	chessboard.printBoard()
	return thingie

def requestPlayerMove(chessboard):
	move = raw_input("Please enter a move:\n")
	valid_move = playerMove(chessboard, move)
	while not valid_move:
		move = raw_input("That is not a valid move. Enter another:\n")
		valid_move = playerMove(chessboard, move)

def main():
	print "Creating Board"
	board = ChessBoard.ChessBoard()
	board_dictionary = None
	#print "Opening Board Dictionary"
	#f = open("Opening_book.txt")
	#board_dictionary = pickle.load(f)
	#f.close()

	AI_color = raw_input("Which color should the AI take? [w/b]\n")
	AI_time = 17
	while AI_color not in 'wb':
		AI_color = raw_input("That is neither 'w' nor 'b'. Try again. [w/b]\n")

	board.printBoard()
	white_turn = True
	while not board.isGameOver():
		if white_turn:
			if AI_color == 'w':
				AI_Move(board, True, AI_time, board_dictionary)
			else:
				requestPlayerMove(board)
		else:
			if AI_color == 'w':
				requestPlayerMove(board)
			else:
				AI_Move(board, False, AI_time, board_dictionary)
		white_turn = not white_turn

	print board.getGameResult()
	raw_input("Press any key to quit.")

if __name__ == '__main__':
	main()


