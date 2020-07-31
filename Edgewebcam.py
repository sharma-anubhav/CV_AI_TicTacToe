import numpy as np
import cv2
import time
from math import inf as infinity
import numpy as np

players = ['X', 'O']

def play_move(state, player, block_num):
    if state[int((block_num - 1) / 3)][(block_num - 1) % 3] is ' ':
        state[int((block_num - 1) / 3)][(block_num - 1) % 3] = player
    else:
        block_num = int(input("Block is not empty, ya blockhead! Choose again: "))
        play_move(state, player, block_num)


def print_board(game_state):
    print('----------------')
    print('| ' + str(game_state[0][0]) + ' || ' + str(game_state[0][1]) + ' || ' + str(game_state[0][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[1][0]) + ' || ' + str(game_state[1][1]) + ' || ' + str(game_state[1][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[2][0]) + ' || ' + str(game_state[2][1]) + ' || ' + str(game_state[2][2]) + ' |')
    print('----------------')


def copy_game_state(state):
    new_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state


def check_current_state(game_state):
    # Check if draw
    draw_flag = 0
    for i in range(3):
        for j in range(3):
            if game_state[i][j] is ' ':
                draw_flag = 1
    if draw_flag is 0:
        return None, "Draw"

    # Check horizontals
    if (game_state[0][0] == game_state[0][1] and game_state[0][1] == game_state[0][2] and game_state[0][0] is not ' '):
        return game_state[0][0], "Done"
    if (game_state[1][0] == game_state[1][1] and game_state[1][1] == game_state[1][2] and game_state[1][0] is not ' '):
        return game_state[1][0], "Done"
    if (game_state[2][0] == game_state[2][1] and game_state[2][1] == game_state[2][2] and game_state[2][0] is not ' '):
        return game_state[2][0], "Done"

    # Check verticals
    if (game_state[0][0] == game_state[1][0] and game_state[1][0] == game_state[2][0] and game_state[0][0] is not ' '):
        return game_state[0][0], "Done"
    if (game_state[0][1] == game_state[1][1] and game_state[1][1] == game_state[2][1] and game_state[0][1] is not ' '):
        return game_state[0][1], "Done"
    if (game_state[0][2] == game_state[1][2] and game_state[1][2] == game_state[2][2] and game_state[0][2] is not ' '):
        return game_state[0][2], "Done"

    # Check diagonals
    if (game_state[0][0] == game_state[1][1] and game_state[1][1] == game_state[2][2] and game_state[0][0] is not ' '):
        return game_state[1][1], "Done"
    if (game_state[2][0] == game_state[1][1] and game_state[1][1] == game_state[0][2] and game_state[2][0] is not ' '):
        return game_state[1][1], "Done"

    return None, "Not Done"


def print_state(game_state):
    print('----------------')
    print('| ' + str(game_state[0][0]) + ' || ' + str(game_state[0][1]) + ' || ' + str(game_state[0][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[1][0]) + ' || ' + str(game_state[1][1]) + ' || ' + str(game_state[1][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[2][0]) + ' || ' + str(game_state[2][1]) + ' || ' + str(game_state[2][2]) + ' |')
    print('----------------')


def getBestMove(state, player):
    '''
    Minimax Algorithm
    '''
    winner_loser, done = check_current_state(state)
    if done == "Done" and winner_loser == 'O':  # If AI won
        return 1
    elif done == "Done" and winner_loser == 'X':  # If Human won
        return -1
    elif done == "Draw":  # Draw condition
        return 0

    moves = []
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if state[i][j] is ' ':
                empty_cells.append(i * 3 + (j + 1))

    for empty_cell in empty_cells:
        move = {}
        move['index'] = empty_cell
        new_state = copy_game_state(state)
        play_move(new_state, player, empty_cell)

        if player == 'O':  # If AI
            result = getBestMove(new_state, 'X')  # make more depth tree for human
            move['score'] = result
        else:
            result = getBestMove(new_state, 'O')  # make more depth tree for AI
            move['score'] = result

        moves.append(move)

    # Find best move
    best_move = None
    if player == 'O':  # If AI player
        best = -infinity
        for move in moves:
            if move['score'] > best:
                best = move['score']
                best_move = move['index']
    else:
        best = infinity
        for move in moves:
            if move['score'] < best:
                best = move['score']
                best_move = move['index']

    return best_move


game = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
cap = cv2.VideoCapture(0)
size = 150  # size of grid


def state():
    timeout = time.time() + 4
    while True:
        ret_val, frame = cap.read()
        frame = cv2.flip(frame, 1)
        x = frame.shape[1] - 3 * size
        y = 0
        evaluate = []
        cv2.putText(frame,"MAKE SURE THE BACKGROUND OF GRID IS PLAIN" , (5,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255),2,cv2.LINE_AA)

        cv2.rectangle(frame, (x, y), (x + size, y + size), (0, 255, 0), 2)
        if game[0][0] != ' ':
            cv2.putText(frame, str(game[0][0]), (x + 40, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2)
        else:
            evaluate.append([frame[y:y + size, x:x + size], 0, 0])

        cv2.rectangle(frame, (x + size, y), (x + 2 * size, y + size), (0, 255, 0), 2)
        if game[0][1] != ' ':
            cv2.putText(frame, str(game[0][1]), (x + size + 40, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2)
        else:
            evaluate.append([frame[y:y + size, x + size:x + 2 * size], 0, 1])

        cv2.rectangle(frame, (x + 2 * size, y), (x + 3 * size, y + size), (0, 255, 0), 2)
        if game[0][2] != ' ':
            cv2.putText(frame, str(game[0][2]), (x + 2 * size + 40, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255),
                        2)
        else:
            evaluate.append([frame[y:y + size, x + 2 * size:x + 3 * size], 0, 2])

        y = y + size

        cv2.rectangle(frame, (x, y), (x + size, y + size), (0, 255, 0), 2)
        if game[1][0] != ' ':
            cv2.putText(frame, str(game[1][0]), (x + 40, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2)
        else:
            evaluate.append([frame[y:y + size, x:x + size], 1, 0])

        cv2.rectangle(frame, (x + size, y), (x + 2 * size, y + size), (0, 255, 0), 2)
        if game[1][1] != ' ':
            cv2.putText(frame, str(game[1][1]), (x + size + 40, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2)
        else:
            evaluate.append([frame[y:y + size, x + size:x + 2 * size], 1, 1])

        cv2.rectangle(frame, (x + 2 * size, y), (x + 3 * size, y + size), (0, 255, 0), 2)
        if game[1][2] != ' ':
            cv2.putText(frame, str(game[1][2]), (x + 2 * size + 40, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255),
                        2)
        else:
            evaluate.append([frame[y:y + size, x + 2 * size:x + 3 * size], 1, 2])

        y = y + size

        cv2.rectangle(frame, (x, y), (x + size, y + size), (0, 255, 0), 2)
        if game[2][0] != ' ':
            cv2.putText(frame, str(game[2][0]), (x + 40, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2)
        else:
            evaluate.append([frame[y:y + size, x:x + size], 2, 0])

        cv2.rectangle(frame, (x + size, y), (x + 2 * size, y + size), (0, 255, 0), 2)
        if game[2][1] != ' ':
            cv2.putText(frame, str(game[2][1]), (x + size + 40, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2)
        else:
            evaluate.append([frame[y:y + size, x + size:x + 2 * size], 2, 1])

        cv2.rectangle(frame, (x + 2 * size, y), (x + 3 * size, y + size), (0, 255, 0), 2)
        if game[2][2] != ' ':
            cv2.putText(frame, str(game[2][2]), (x + 2 * size + 40, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255),
                        2)
        else:
            evaluate.append([frame[y:y + size, x + 2 * size:x + 3 * size], 2, 2])

        cv2.imshow('IDK', frame)

        if time.time() > timeout:
            break
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    return evaluate

def playermove(evaluate):
    for image, i, j in evaluate:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(grey.copy(), 105, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        print(len(contours), i, j)
        if len(contours) > 0:
            game[i][j] = 'X'
            return game

winner = "Human"
current_state = "Not Done"
while True:
    evaluate = state()
    playermove(evaluate)
    winner, current_state = check_current_state(game)
    if current_state != "Not Done":
        if current_state == "Draw":
            winner = "Draw"
            break
        else:
            winner = "Human"
            break
    AI = getBestMove(game, 'O')
    game[int((AI - 1) / 3)][(AI - 1) % 3] = 'O'
    winner, current_state = check_current_state(game)
    if current_state != "Not Done":
        if current_state == "Draw":
            winner = "Draw"
            break
        else:
            winner = "Computer"
            break


while True:
    ret_val, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, str(winner), (0, frame.shape[1]//2), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5,cv2.LINE_AA)
    cv2.imshow('IDK', frame)

    if cv2.waitKey(1) == 27:
        break  # esc to quit

cv2.destroyAllWindows()
