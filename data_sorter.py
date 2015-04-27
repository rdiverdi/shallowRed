""" This is meant to simplify our dictionaries, and separate them into black and white
	datasets."""
import pickle

file_list = []
for i in range(1999,2013):
	file_list.append(str(i) + '_data.txt')

Giant_White_Dataset = {}
Giant_Black_Dataset = {}

for filename in file_list:
	f = open(filename, 'r')
	board_dictionary = pickle.load(f)
	f.close()

	for board_state in board_dictionary:
		move_dict = board_dictionary[board_state]
		if board_state[1] == True: #Checks to see if it's a board that White moves on
			if board_state[0] not in Giant_White_Dataset:
				Giant_White_Dataset[board_state[0]] = move_dict
			else:
				for move in move_dict:
					if move in Giant_White_Dataset[board_state[0]]: 
						#Updates the [win, loss, draw] results of a move for a given board
						Giant_White_Dataset[board_state[0]][move][0] += move_dict[move][0]
						Giant_White_Dataset[board_state[0]][move][1] += move_dict[move][1]
						Giant_White_Dataset[board_state[0]][move][2] += move_dict[move][2]
					else:
						Giant_White_Dataset[board_state[0]][move] = move_dict[move]
		else:
			if board_state[0] not in Giant_Black_Dataset:
				Giant_Black_Dataset[board_state[0]] = move_dict
			else:
				for move in move_dict:
					if move in Giant_Black_Dataset[board_state[0]]: 
						#Updates the [win, loss, draw] results of a move for a given board
						Giant_Black_Dataset[board_state[0]][move][0] += move_dict[move][0]
						Giant_Black_Dataset[board_state[0]][move][1] += move_dict[move][1]
						Giant_Black_Dataset[board_state[0]][move][2] += move_dict[move][2]
					else:
						Giant_Black_Dataset[board_state[0]][move] = move_dict[move]

f = open('Giant_Black_Dataset.txt', 'w')
pickle.dump(Giant_Black_Dataset, f)
f.close()

f = open('Giant_White_Dataset.txt', 'w')
pickle.dump(Giant_White_Dataset, f)
f.close()