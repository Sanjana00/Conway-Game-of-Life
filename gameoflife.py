from random import randint

# board is of dimensions M x N

M = randint(3, 5)
N = randint(3, 5)
DEAD = '.'
LIVE = 'O'

def generate_board():
    board = [[DEAD for i in range(N)] for j in range(M)]
    for row, line in enumerate(board):
        for col, cell in enumerate(line):
            board[row][col] = get_cell() #populating board
    return board

def get_cell():
    if randint(0, 2) == 0:
        return LIVE
    return DEAD

def add_sentinels(board):
    board = [[DEAD] + row + [DEAD] for row in board]
    n = len(board[0])
    board.append([DEAD] * (n + 2))
    board.insert(0,[DEAD] * (n + 2))
    return board

def remove_sentinels(board):
    return [row[1:-1] for row in board[1:-1]]

def next_state(board):
    duplicate_board = [row[:] for row in board]
    for row, line in enumerate(board[1:-1]):
        for col, cell in enumerate(line[1:-1]):
            duplicate_board[row + 1][col + 1] = get_state(board[row + 1][col + 1], count_live_neighbours(row + 1, col + 1, board))
    return duplicate_board

def get_state(cell, num_live):
    if cell == LIVE:
        if num_live in [2, 3]:
            return LIVE
        return DEAD
    if num_live == 3:
        return LIVE
    return DEAD

def count_live_neighbours(row, col, board):
    neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [board[row - neighbour[0]][col - neighbour[1]] for neighbour in neighbours].count(LIVE)

def display_board(board):
    for row in board:
        print(' '.join(row))

def expand_vertical(board):
    if LIVE in board[0]:
        board.insert(0, [DEAD] * len(board[0]))
    if LIVE in board[-1]:
        board.append([DEAD] * len(board[0]))
    return board

def expand_horizontal(board):
    if any([row[0] == LIVE for row in board]):
        board = [[DEAD] + row for row in board]
    if any([row[-1] == LIVE for row in board]):
        board = [row + [DEAD] for row in board]
    return board

def expand(board):
    return expand_horizontal(expand_vertical(board))

def contract_vertical(board):
    while LIVE not in board[0] and LIVE not in board[1] and len(board) > 2:
        board = board[1:]
    while LIVE not in board[-1] and LIVE not in board[-2] and len(board) > 2:
        board = board[:-1]
    return board

def contract_horizontal(board):
    while all([row[0] == DEAD and row[1] == DEAD for row in board]) and len(board[0]) > 2:
        board = [row[1:] for row in board]
    while all([row[-1] == DEAD and row[-2] == DEAD for row in board]) and len(board[0]) > 2:
        board = [row[:-1] for row in board]
    return board

def contract(board):
    return contract_horizontal(contract_vertical(board))

def is_termination(board, history):
    return add_sentinels(board) in history or all([row.count(LIVE) == 0 for row in board]) or all([row.count(DEAD) == 0 for row in board])


# driver code

game_history = []
# board = contract(expand([['O', 'O', 'O']])) //blinker test
board = contract(expand(generate_board()))
display_board(board)

print()

board = add_sentinels(board)
game_history.append(board)

choice = 'Y'
while choice == 'Y':
    board = contract(expand(remove_sentinels(next_state(board))))

    print()
    display_board(board)
    print()
    if is_termination(board, game_history):
        choice = 'N'
    else:
        print('Generate next state? [y/n]:', end=' ')
        choice = input().upper()
        board = add_sentinels(board)
        game_history.append(board)

