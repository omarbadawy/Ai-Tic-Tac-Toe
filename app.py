import time
from random import choice
import platform
from os import system


HUMAN = -1
COMP = +1

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells

def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

def set_move(x,y, player):
    if valid_move(x,y):
        board[x][y] = player
        return True
    else:
        return False

def render_board(state, hum, com):
    for row in state:
        string = '|'
        for col in row:
            symbol = '-'
            if col == 1:
                symbol = com
            elif col == -1:
                symbol = hum
            string = string + ' ' + symbol + ' |'
        print('-------------')
        print(string)
    print('-------------')

def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score

def minimax(state, depth, player):
    if (player == COMP):
        best = [-1, -1, -1000]
    else:
        best = [-1, -1, +1000]
    
    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]
    
    for cell in empty_cells(state):
        x, y = cell
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if best[2] < score[2]:
                best = score
        else:
            if best[2] > score[2]:
                best = score
    return best

def ai_turn(c_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
    
    print(f'Computer turn [{c_choice}]')
    
    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]
    
    set_move(x, y, COMP)
    time.sleep(.8)



def human_turn(h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
    
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    print(f'Human turn [{h_choice}]')

    while move < 1 or move > 9:
        try:
            move = int(input('Enter number [1:9]: '))
            coordinates = moves[move]
            can_move = set_move(coordinates[0], coordinates[1], HUMAN)

            if not can_move:
                move = -1
                print('Bad move, Try Again!')
        except:
            print('Try again!')

def play(human_c):
    print('Initial State!')
    comp_c = 'O' if human_c == 'X' else 'X'
    render_board(board, human_c, comp_c)
    while not game_over(board):
        if len(empty_cells(board)) == 0:
            print('Draw!')
            break
        
        if human_c == 'X':
            human_turn(human_c)
            clean()
            render_board(board, human_c, comp_c)
            ai_turn(comp_c)
            clean()
            render_board(board, human_c, comp_c)
            
        elif human_c == 'O':
            ai_turn(comp_c)
            clean()
            render_board(board, human_c, comp_c)
            human_turn(human_c)
            clean()
            render_board(board, human_c, comp_c)
    
    if game_over(board):
        score = evaluate(board)
        if score == 0:
            print('Draw..............')
        elif score == 1:
            print('Computer wins!')
        else:
            print('Player wins!')

play('X')