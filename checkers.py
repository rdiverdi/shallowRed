import numpy as np


class board(object):
    def __init__(self, game):
        self.board = np.zeros((8, 8))
        self.turn = 1

        if game == 'checkers':
            for i, row in enumerate (self.board):
                piece = 0
                if i <= 2:
                    piece = 1
                if i >= 5:
                    piece = -1
                if piece != 0:
                    for j in range(len(row)):
                        if i%2 != j%2:
                            self.board[i][j] = piece

    def change_turn(self):
        self.turn *= -1

    def move(self, col, row, new_col, new_row):
        """
        Take an initial piece (column letter, row number)
        and a final position (column ltter, row number)
        checks if move is legal and makes move if it is legal
        """
        letters = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        #colors = {'red':1, 'black':-1}

        #convert from english to code
        row = row -1
        col = letters[col]
        new_row = new_row -1
        new_col = letters[new_col]

        if self.board[new_row][new_col] == 0:
            if self.board[row][col] * self.turn >= 1:
                if new_row - row == self.turn and abs(new_col - col) == 1:
                    self.change_to(col, row, 0)
                    self.change_to(new_col, new_row, self.turn)
                    self.change_turn()
                elif new_row - row == 2*self.turn and abs(new_col - col) == 2 and\
                     self.board[row + self.turn][(col + new_col)/2] == -1*self.turn:
                    self.change_to(col, row, 0)
                    self.change_to(new_col, new_row, self.turn)
                    self.change_to((col + new_col)/2, row + self.turn, 0)
                    self.change_turn()
                else:
                    print "not a legal move"
            #if self.board[row][col] * self.turn >= 2
            #TODO: 2's (and -2's) will be kinged pieces, check for newly allwoed moves

            else:
                print "you don't have a piece there"
        else:
            print "there is already a piece where you want to go"

    def change_to(self, column, row, color):
        """
        Take a column number and a row number
        makes the indicated place the indicated number
        """

        self.board[row][column] = color

checkers = board('checkers')

print checkers.turn
checkers.move('d', 3, 'e', 4)
print checkers.turn
#checkers.move('g', 3, 'f', 6)
checkers.move('g', 6, 'f', 5)
print checkers.turn
checkers.move('e', 4, 'g', 6)
print checkers.board