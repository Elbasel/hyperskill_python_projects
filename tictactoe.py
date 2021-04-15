def print_grid(cells):
    print("""
    ---------
    | {} {} {} |
    | {} {} {} |
    | {} {} {} |
    ---------
    """.format(*cells.upper()))


def get_state(cells):

    cells = cells.lower()
    # analyze cells
    rows = [list(cells[i: i + 3]) for i in range(0, 7, 3)]
    cols = [[row[i] for row in rows] for i in range(3)]
    first_diagonal = [[row[i] for i, row in enumerate(rows)]]
    second_diagonal = [[row[-i - 1] for i, row in enumerate(rows)]]

    winning_intervals = rows + cols + first_diagonal + second_diagonal

    # one of the players took more turns than the other one
    num_o = cells.count('o')
    num_x = cells.count('x')
    if abs(num_x - num_o) >= 2:
        return 'Impossible'

    # check who won
    x_wins = o_wins = False
    for interval in winning_intervals:
        if len(set(interval)) == 1:
            if interval[0] == 'x':
                x_wins = True
            elif interval[0] == 'o':
                o_wins = True

    # both wins
    if x_wins and o_wins:
        return 'Impossible'

    # neither player won and there is at least one empty cell
    if not (x_wins or o_wins) and ('_' in cells):
        return 'Game not finished'
    # neither player on and there are no empty cells
    elif not (x_wins or o_wins) and not ('_' in cells):
        return 'Draw'

    if x_wins:
        return 'X wins'
    elif o_wins:
        return 'O wins'

    return 'NO STATE'

def get_input():
    while True:
        coordinates = input('Enter coordinates: ')
        try:
            x, y = tuple(map(int, coordinates.split()))
        except ValueError:
            print('You should enter numbers!')
            continue
        if not ((0 < x < 4) and (0 < y < 4)):
            print('Coordinates should be from 1 to 3!')
            continue
        elif grid[x - 1][y - 1] != '_':
            print('This cell is occupied! Choose another one!')
            continue

        return x, y

cells = '_________'
print_grid(cells)

grid = [list(cells[i: i + 3]) for i in range(0, 7, 3)]

i = 1
while True:
    i += 1
    x, y = get_input()

    if i % 2 == 0:
        player = 'X'
    else:
        player = 'O'


    grid[x - 1][y - 1] = player
    cells = ''.join([elem for row in grid for elem in row])
    print_grid(cells)
    state = get_state(cells)
    if state != 'Game not finished':
        print(state)
        break