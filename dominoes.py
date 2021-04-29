from itertools import combinations_with_replacement
from random import sample, choice


def get_starting_board():
    domino = list(map(lambda x: list(x), combinations_with_replacement(range(7), 2)))
    while True:
        player_pieces = sample(domino, 7)
        computer_pieces = sample(list(filter(lambda x: x not in player_pieces, domino)), 7)
        stock_pieces = list(filter(lambda x: x not in (player_pieces + computer_pieces), domino))
        player_doubles = [piece for piece in player_pieces if len(set(piece)) == 1]
        computer_doubles = [piece for piece in computer_pieces if len(set(piece)) == 1]
        doubles = player_doubles + computer_doubles
        if doubles:
            highest_double = max(doubles)
            if highest_double in player_doubles:
                player_pieces.remove(highest_double)
                first_player = 'computer'
            else:
                computer_pieces.remove(highest_double)
                first_player = 'player'
            return {'player': player_pieces, 'computer': computer_pieces,
                    'stock': stock_pieces, 'snake': [highest_double],
                    'turn': first_player}


def get_board_status():
    if len(board['player']) == 0:
        return 'The game is over. You won!'
    elif len(board['computer']) == 0:
        return 'The game is over. The computer won!'
    flat_snake = [num for piece in board['snake'] for num in piece]  # Flatten the 2-dimensional list into one list
    for i in range(7):
        if i in board['snake'][0] and i in board['snake'][-1] and flat_snake.count(i) == 8:
            return "The game is over. It's a draw!"
    return 'game_not_done'


def display_board():
    print('=' * 70)
    print('Stock size:', len(board['stock']))
    print('Computer pieces:', len(board['computer']))
    print()
    snake = board['snake']
    if len(snake) > 6:
        for i in range(3):
            print(snake[i], end='')
        print('...', end='')
        for i in range(-3, 0):
            print(snake[i], end='')
        print()
    else:
        for p in snake:
            print(p, end='')
    print()
    print('\nYour pieces:')
    for i, piece in enumerate(board['player']):
        print(f'{i+1}:{piece}')
    print()


def is_valid_move(move, player):
    try:
        move = int(move)
    except ValueError:
        return False, 'invalid'

    if move == 0:
        if len(board['stock']) > 0:
            return True, 'valid_legal'
        else:
            return False, 'invalid'

    if not len(board[player]) >= abs(move):
        return False, 'invalid'

    index = abs(move) - 1
    piece = board[player][index]
    if move > 0:
        for num in piece:
            if num == board['snake'][-1][1]:
                break
        else:
            return False, 'illegal'
    else:
        for num in piece:
            if num == board['snake'][0][0]:
                break
        else:
            return False, 'illegal'

    return True, 'valid_legal'




def make_move(move, player):
    """
    player: can either be "player" or "computer"
    """
    if move == 0:
        stock_piece = choice(board['stock'])
        board['stock'].remove(stock_piece)
        board[player].append(stock_piece)
        return
    index = abs(move) - 1
    piece = board[player][index]
    board[player].remove(piece)
    if move > 0:
        if board['snake'][-1][1] != piece[0]:
            piece = piece[::-1]
        board['snake'].append(piece)
    else:
        if board['snake'][0][0] != piece[1]:
            piece = piece[::-1]
        board['snake'].insert(0, piece)


def generate_computer_move():
    field = []
    for x in (board['snake'] + board['computer']):
        field.append(x[0])
        field.append(x[1])
    counts = {num: field.count(num) for num in range(7)}
    scores = {}
    for piece in board['computer']:
        score = counts[piece[0]] + counts[piece[1]]
        scores[tuple(piece)] = score
    scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
    for piece, score in scores.items():
        piece_index = board['computer'].index(list(piece)) + 1
        if is_valid_move(piece_index, 'computer')[0]:
            return piece_index
        elif is_valid_move(-piece_index, 'computer')[0]:
            return -piece_index
    else:
        return 0

board = get_starting_board()
while True:
    display_board()
    game_state = get_board_status()

    if game_state != 'game_not_done':
        print('Status:', game_state)
        break

    turn = board['turn']
    if turn == 'player':
        print("Status: It's your turn to make a move. Enter your command.")
        while True:
            move = input()
            valid_move, code = is_valid_move(move, board['turn'])
            if valid_move:
                break
            if code == 'invalid':
                print('invalid input. please try again.')
            else:
                print('illegal move. please try again')
        move = int(move)
        board['turn'] = 'computer'
    else:
        input('Status: Computer is about to make a move. Press Enter to continue...\n')
        move = generate_computer_move()
        board['turn'] = 'player'

    make_move(move, turn)

