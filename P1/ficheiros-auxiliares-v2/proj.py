from search import *
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

"""Models a Solitaire problem as a satisfaction problem.
 A solution cannot have more than 1 peg left on the board."""
class solitaire(Problem):
    def __init__(self, board):
        self.initial = sol_state(board)
    def actions(self, state):
        return
    def result(self, state, action):
        return
    def goal_test(self, state):
        return

    def path_cost(self, c, state1, action, state2):
        return c + 1
    def h(self, node):
        return
"""Needed for informed search."""
class sol_state():
    def __init__(self, board):
        self.board = board
        self.numberOfPegs = self.countPegs(board)

    def __lt__(self, other):
        self.numberOfPegs < other.numberOfPegs
    
    def countPegs():
        pegs = 0
        for line in board:
            for content in line:
                if is_peg(content):
                    pegs += 1

def is_board_move_down(pos, board):
    return is_peg(board[pos_l(pos) + 1][pos_c(pos)]) and is_empty(board[pos_l(pos) + 2][pos_c(pos)])

def is_board_move_right(pos, board):
    return is_peg(board[pos_l(pos)][pos_c(pos) + 1]) and is_empty(board[pos_l(pos)][pos_c(pos) + 2])

def is_board_move_left(pos, board):
    return is_peg(board[pos_l(pos)][pos_c(pos) - 1]) and is_empty(board[pos_l(pos)][pos_c(pos) - 2])

def is_board_move_up(pos, board):
    return is_peg(board[pos_l(pos) - 1][pos_c(pos)]) and is_empty(board[pos_l(pos) - 2][pos_c(pos)])

b1 = [["_","O","O","O","_"], ["O","_","O","_","O"], ["_","O","_","O","_"],
 ["O","_","O","_","_"], ["_","O","_","_","_"]] 

def board_perform_move(board, move):
    init = move[0]
    end = move[1]
    if pos_l(end) == pos_l(init):
        if end < init:
            pegEaten = make_pos(pos_l(end), pos_c(end) + 1)
        else:
            pegEaten = make_pos(pos_l(end), pos_c(init) + 1)
    else:
        if end < init:
            pegEaten = make_pos(pos_l(end) + 1, pos_c(end))
        else:
            pegEaten = make_pos(pos_l(init) + 1, pos_c(end))
    #pegEaten = make_pos(int(math.fabs(pos_l(end) - pos_l(init))), int(math.fabs(pos_c(end) - pos_c(init))))
    print(pegEaten)
    newBoard = []
    lines = len(board)
    columns = len(board[0])
    for line in range(lines):
        newLine = []
        for column in range(columns):
            pos = make_pos(line, column)
            newLine.append(board[pos_l(pos)][pos_c(pos)])
        newBoard.append(newLine)
    print(pos_l(init), pos_c(init))
    newBoard[pos_l(init)][pos_c(init)] = c_empty()
    newBoard[pos_l(pegEaten)][pos_c(pegEaten)] = c_empty()
    newBoard[pos_l(end)][pos_c(end)] = c_peg()
    return newBoard

def board_moves(board):
    lines = len(board)
    columns = len(board[0])
    moves = []
    for line in range(lines):
        for column in range(columns):
            if is_peg(board[line][column]):
                if line < 2:
                    print("line < 2", line, column)
                    if is_board_move_down(make_pos(line, column), board):
                        print("mv down", line, column)
                        moves.append([make_pos(line, column), make_pos(line + 2, column)])
                elif line > lines - 3:
                    if is_board_move_up(make_pos(line, column), board):
                        moves.append([make_pos(line, column), make_pos(line, column - 2)])
                else:
                    if is_board_move_down(make_pos(line, column), board):
                        moves.append([make_pos(line, column), make_pos(line + 2, column)])
                    if is_board_move_up(make_pos(line, column), board):
                        moves.append([make_pos(line, column), make_pos(line, column - 2)])
                if column < 2:
                    if is_board_move_right(make_pos(line, column), board):
                        moves.append([make_pos(line, column), make_pos(line, column + 2)])
                elif column > columns - 3:
                    if is_board_move_left(make_pos(line,column), board):
                        moves.append([make_pos(line, column), make_pos(line, column - 2)])
                else:
                    if is_board_move_right(make_pos(line, column), board):
                        moves.append([make_pos(line, column), make_pos(line, column + 2)])
                    if is_board_move_left(make_pos(line,column), board):
                        moves.append([make_pos(line, column), make_pos(line, column - 2)])
    return moves

print(board_moves(b1))