"""I'm just testing things. This lets you play the basic chess algorithm that I made. You'll beat it. It's inevitable, really."""
import ChessBoard
import MinMax
import time

def makeBoard():
	return ChessBoard.ChessBoard()

def AI_Move(chessboard, white, max_time):
	evaluation = MinMax.BoardEvaluation(chessboard, white, MinMax.evaluate_board)
	curr_time = time.time()
	AI_move = evaluation.evaluate(max_time)
	print "Turn calculation took: " + str(curr_time - time.time()) + " seconds"
	chessboard.addMove(AI_move[0], AI_move[1])
	chessboard.printBoard()

def playerMove(chessboard, move):
	thingie = chessboard.addTextMove(move)
	
	return thingie

