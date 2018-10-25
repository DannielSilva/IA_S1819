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

def filterPegs(move) :
    canMove = []
    for movements in move:
        if move_initial(movements[0]) not in canMove:
            canMove.append(move_initial(movements[0]))
    return len(canMove)

def corner(movements,center):
    count = 0
    for move in movements:
        if (dist(move_final(move),center)>dist(move_initial(move),center)):
            count += 1
    return count   

def dist(pos1,pos2):
    return math.pow((pos_l(pos1)-pos_l(pos2)),2) + math.pow((pos_c(pos1)-pos_c(pos2)),2)


def isolated_peg(board,pos):
    if(pos_l(pos)<len(board)-2):
        check = check_d_moves(pos,board)
        if (check!=[]):
            return False
    if(pos_l(pos)>1):
        check = check_u_moves(pos,board)
        if (check!=[]):
            return False
    if(pos_c(pos)<len(board[0])-2):
        check = check_r_moves(pos,board)
        if (check!=[]):
            return False
    if(pos_c(pos)>1):
        check = check_l_moves(pos,board)
        if (check!=[]):
            return False
    return True

def isolated_pegs(board,lines,collums):
    count = 0
    for i in range(0,lines):
        for j in range(0,collums):
            if isolated_peg(board,make_pos(i,j)):
                count += 1
    return count

"""Models a Solitaire problem as a satisfaction problem.
 A solution cannot have more than 1 peg left on the board."""
class solitaire(Problem):

    def __init__(self, board):
        super().__init__(self,board)
        self.initial = sol_state(board)
        self.lines = len(board)
        self.collumns = len(board[0])

    def actions(self, state):
        return board_moves(state.board)

    def result(self, state, action):
        return sol_state(board_perform_move(state.board,action))

    def goal_test(self, state):
        return state.countPegs() == 1

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):

        #return ((node.state.countPegs()*2)-len(board_moves(node.state.board)))*(node.state.countPegs() -1)
 
        #print(corner(board_moves(node.state.board),(self.lines/2,self.collumns/2)) + isolated_pegs(node.state.board,self.lines,self.collumns) - filterPegs(board_moves(node.state.board)) , end=' ')
        ##return corner(board_moves(node.state.board),(self.lines/2,self.collumns/2)) + isolated_pegs(node.state.board,self.lines,self.collumns) - filterPegs(board_moves(node.state.board))  
        #return  (2*node.state.countPegs() -1 - filterPegs(board_moves(node.state.board)))
        return (len(node.state.board)*len(node.state.board[0])-len(board_moves(node.state.board)))*(node.state.countPegs() -1)
 


b1 = [["_","O","O","O","_"], ["O","_","O","_","O"], ["_","O","_","O","_"],
 ["O","_","O","_","_"], ["_","O","_","_","_"]] 

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

def board_moves(board):
    moves = []
    for i in range(0,len(board)):
        for j in range(0,len(board[0])):
            pos = make_pos(i,j)
            if (is_peg(board[i][j])):
                moves += check_moves(pos,board)
               
    return moves




m4x4 = [["O","O","O","X"],
        ["O","O","O","O"],
        ["O","_","O","O"],
        ["O","O","O","O"]]      

m4x5 = [["O","O","O","X","X"],
        ["O","O","O","O","O"],
        ["O","_","O","_","O"],
        ["O","O","O","O","O"]]

m5x5 = [["_","O","O","O","_"],
        ["O","_","O","_","O"],
        ["_","O","_","O","_"],
        ["O","_","O","_","_"],
        ["_","O","_","_","_"]]

m4x6 = [["O","O","O","X","X","X"],
        ["O","_","O","O","O","O"],
        ["O","O","O","O","O","O"],
        ["O","O","O","O","O","O"]] 

"""def test(board):
    start = time.time()
    print("greedy_search: ", greedy_search(solitaire(board)).state.board)
    end1 = time.time()
    print("  Time: ",end1 - start)

    print("depth_first_tree_search: ", depth_first_tree_search(solitaire(board)).state.board)
    end2 = time.time()
    print("  Time: ",end2 - end1)

    
    print("astar_search: ", astar_search(solitaire(board)).state.board)
    end3 = time.time()
    print("  Time: ",end3 - end2)

test(m4x5) """
matrixes = [m4x4, m4x5, m5x5]

def register(matrixes):
    for m in matrixes:
        game = solitaire(m)
        problem = InstrumentedProblem(game)
        start = time.time()
        greedy_search(problem)
        print("greedy_search: ", problem)
        end1 = time.time()
        print("  Time: ",end1 - start)
        print(problem)

        game = solitaire(m)
        problem = InstrumentedProblem(game)
        end1 = time.time()
        depth_first_tree_search(problem)
        print("depth_first_tree_search: ", problem)
        end2 = time.time()
        print("  Time: ",end2 - end1)
        print(problem)

        game = solitaire(m)
        problem = InstrumentedProblem(game)
        end2 = time.time()
        astar_search(problem)
        print("astar_search: ", problem)
        end3 = time.time()
        print("  Time: ",end3 - end2)
        
        print(problem)

register(matrixes)



game = solitaire(m4x6)
problem = InstrumentedProblem(game)
start = time.time()
greedy_search(problem)
print("greedy_search: ", problem)
end1 = time.time()
print("  Time: ",end1 - start)




game = solitaire(m4x6)
problem = InstrumentedProblem(game)
end2 = time.time()
astar_search(problem)
print("astar_search: ", problem)
end3 = time.time()
print("  Time: ",end3 - end2)