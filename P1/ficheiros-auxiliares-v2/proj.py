"""
86409 Diogo Pereira
86445 Joao Daniel Silva
Grupo 40
"""
from search import *
import time
import math

# TAI content
def c_peg  ():
		return "O"
def c_empty():
		return "_"
def c_blocked():
 return "X"
def is_empty(e):
		return e == c_empty()
def is_peg(e):
		return e == c_peg()
def is_blocked(e):
		return e == c_blocked()

# TAI pos
# Tuplo (l, c)
def make_pos(l, c):
		return (l, c)
def pos_l(pos):
		return pos[0]
def pos_c(pos):
		return pos[1]

# TAI move
# Lista [p_initial, p_final]
def make_move(i, f):
		return [i, f]
def move_initial(move):
		return move[0]
def move_final(move):
		return move[1]



"""Needed for informed search."""
class sol_state():
		def __init__(self, board):
				self.board = board
				
		def __lt__(self, other):
				return self.countPegs() > other.countPegs()
		
		def countPegs(self):
				pegs = 0
				for line in self.board:
						for content in line:
								if is_peg(content):
										pegs += 1
				return pegs


"""Models a Solitaire problem as a satisfaction problem.
 A solution cannot have more than 1 peg left on the board."""
class solitaire(Problem):

		def __init__(self, board):
				super().__init__(self,board)
				self.initial = sol_state(board)

		def actions(self, state):
				return board_moves(state.board)

		def result(self, state, action):
				return sol_state(board_perform_move(state.board,action))

		def goal_test(self, state):
				return state.countPegs() == 1

		def path_cost(self, c, state1, action, state2):
				return c + 1

		def h(self, node):
				""" Number of impossible movements plus the number of pegs that cannot move
					impossible movements = 2*node.state.countPegs()- len(board_moves(node.state.board)) 
					pegs that cannot move = node.state.countPegs() - filterPegs(board_moves(node.state.board)) """
				return  3*node.state.countPegs() -1 -len(board_moves(node.state.board))-filterPegs(board_moves(node.state.board))

""" Returns a new board which is the state of the board after perfoming a valid movement
	Moves a peg to its new position and removes the peg that was removed by the former """		
def board_perform_move(board, move):

		if pos_l(move_final(move)) == pos_l(move_initial(move)):
				if move_final(move) < move_initial(move):
						pegEaten = make_pos(pos_l(move_final(move)), pos_c(move_final(move)) + 1)
				else:
						pegEaten = make_pos(pos_l(move_final(move)), pos_c(move_initial(move)) + 1)
		else:
				if move_final(move) < move_initial(move):
						pegEaten = make_pos(pos_l(move_final(move)) + 1, pos_c(move_final(move)))
				else:
						pegEaten = make_pos(pos_l(move_initial(move)) + 1, pos_c(move_final(move)))

		newBoard = []
		lines = len(board)
		columns = len(board[0])
		for line in range(lines):
				newLine = []
				for column in range(columns):
						pos = make_pos(line, column)
						newLine.append(board[pos_l(pos)][pos_c(pos)])
				newBoard.append(newLine)

		newBoard[pos_l(move_initial(move))][pos_c(move_initial(move))] = c_empty()
		newBoard[pos_l(pegEaten)][pos_c(pegEaten)] = c_empty()
		newBoard[pos_l(move_final(move))][pos_c(move_final(move))] = c_peg()
		return newBoard

""" Returns all movements a given peg can make in a given board 
	the functions above are used to specify which direction the peg can move"""
def check_moves(pos,board):
		moves = []
		if(pos_l(pos)<len(board)-2):
				check = check_d_moves(pos,board)
				if (check!=[]):
						moves.append(check)
		if(pos_l(pos)>1):
				check = check_u_moves(pos,board)
				if (check!=[]):
						moves.append(check)
		if(pos_c(pos)<len(board[0])-2):
				check = check_r_moves(pos,board)
				if (check!=[]):
						moves.append(check)
		if(pos_c(pos)>1):
				check = check_l_moves(pos,board)
				if (check!=[]):
						moves.append(check)
		return moves


def check_d_moves(pos,board):
		if(is_peg(board[pos_l(pos)+1][pos_c(pos)]) and is_empty(board[pos_l(pos)+2][pos_c(pos)]) ):
				return [pos,make_pos(pos_l(pos)+2,pos_c(pos))]
		return []

def check_u_moves(pos,board):
		if(is_peg(board[pos_l(pos)-1][pos_c(pos)]) and is_empty(board[pos_l(pos)-2][pos_c(pos)]) ):
				return [pos,make_pos(pos_l(pos)-2,pos_c(pos))]
		return []

def check_r_moves(pos,board):
		if(is_peg(board[pos_l(pos)][pos_c(pos)+1]) and is_empty(board[pos_l(pos)][pos_c(pos)+2])  ):
				return [pos,make_pos(pos_l(pos),pos_c(pos)+2)]
		return []
		
def check_l_moves(pos,board):
		if(is_peg(board[pos_l(pos)][pos_c(pos)-1]) and is_empty(board[pos_l(pos)][pos_c(pos)-2]) ):
				return [pos,make_pos(pos_l(pos),pos_c(pos)-2)]
		return []

""" Returns a list with valid movements   """ 
def board_moves(board):
		moves = []
		for i in range(0,len(board)):
				for j in range(0,len(board[0])):
						pos = make_pos(i,j)
						if (is_peg(board[i][j])):
								moves += check_moves(pos,board)
							 
		return moves

""" Returns the number of pegs that can make a valid move in the current board state """
def filterPegs(move) :
		canMove = []
		for movements in move:
				if move_initial(movements) not in canMove:
						canMove.append(move_initial(movements))
		return len(canMove)

