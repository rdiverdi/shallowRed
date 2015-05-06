# shallowRed
###Chess AI that uses Min/Max search and a dictionary of moves to generate the best move for the respective turn 

####Required Libraries
#####none

####Installation

#####Download all files to play the game
#####Chessboard.py creates the Chess game with board and rules
#####MinMax.py contains the algorithms for using Min/Max search trees and alpha-beta pruning to find the best move. It also evaluates moves
#####PlayMinMax.py plays the moves in the chess game board

####How to use
#####Open Terminal
#####Run PlayMinMax.py
#####Enter "w" or "b" as the color for the AI
#####When it is your turn, enter your move as a string of starting location to end location. For example, to move the piece in a2 to a4, enter "a2a4" (use lowercase only)
#####When it is the AI's turn, the AI will make a move in about 15 seconds and display the end result, levels of the Min/Max tree it traveled, and time taken
#####The board will reprint the current position at the end of each move

####Acknowledgments
#####Credit to John Eriksson for the base implementation of the Chess board with rules
#####Credit to Michael and Dennis for additional optiminizations made to the board
