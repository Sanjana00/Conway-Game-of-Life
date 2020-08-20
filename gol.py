
from random import randint

# board is of dimensions M x N

M = randint(3, 5)
N = randint(3, 5)
DEAD = '.'
LIVE = 'O'

SUSTAIN = [2, 3]
GENERATE = 3

def generate_live_pos():
    live_pos = []
    for row in range(M):
        for col in range(N):
            if get_cell() == LIVE:
                live_pos += [(row, col)]
    return live_pos

def get_cell():
    if randint(0, 2) == 0:
        return LIVE
    return DEAD

def get_neighbours(row, col):
    neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(row + neighbour[0], col + neighbour[1]) for neighbour in neighbours]

def count_live_neighbours(row, col, live_pos):
    return [neighbour in live_pos for neighbour in get_neighbours(row, col)].count(True)

def live_cells(live_pos):
    return [coord for coord in live_pos if count_live_neighbours(coord[0], coord[1], live_pos) in SUSTAIN]

def dead_cells(live_pos):
    neighbours = []
    for pos in live_pos:
        neighbours.extend(get_neighbours(pos[0], pos[1]))
    return [coord for coord in set(neighbours) if neighbours.count(coord) == GENERATE and coord not in live_pos]

def next_generation(live_pos):
    return live_cells(live_pos) + dead_cells(live_pos)

def limits(live_pos):
    if len(live_pos) == 0:
        return 0, 0, 0, 0
    return min(x for x, y in live_pos), max(x for x, y in live_pos), min(y for x, y in live_pos), max(y for x, y in live_pos)

def reorient(live_pos):
    x1, x2, y1, y2 = limits(live_pos)
    return [(x - x1, y - y1) for x, y in live_pos]

def display_board(live_pos):
    x1, x2, y1, y2 = limits(live_pos)
    for i in range(x1 - 1, x2 + 2):
        for j in range(y1 - 1, y2 + 2):
            if (i, j) in live_pos:
                print(LIVE, end=' ')
            else:
                print(DEAD, end=' ')
        print()

def is_termination(live_pos, game_history):
    return len(live_pos) == 0 or reorient(live_pos) in game_history

# driver code

game_history = []
live_pos = generate_live_pos()
# live_pos = [(0, 0), (0, 1), (1, 0), (1, 1)]
# live_pos = [(0, 0), (0, 1), (0, 2)]
display_board(live_pos)
game_history.append(reorient(live_pos))

choice = 'Y'
while choice == 'Y':
    live_pos = next_generation(live_pos)
    print()
    display_board(live_pos)
    print()
    if is_termination(live_pos, game_history):
        choice = 'N'
    else:
        game_history.append(reorient(live_pos))
        print('Generate next state? [y/n]:', end=' ')
        choice = input().upper()
