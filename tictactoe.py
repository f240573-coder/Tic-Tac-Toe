import math

board = [' '] * 9

def print_board():
    print()
    for i in range(3):
        print(f" {board[i*3]} | {board[i*3+1]} | {board[i*3+2]} ")
        if i < 2:
            print("---|---|---")
    print()

def get_empty():
    return [i for i in range(9) if board[i] == ' ']

def check_winner(b):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for w in wins:
        if b[w[0]] == b[w[1]] == b[w[2]] != ' ':
            return b[w[0]]
    return None

def is_full(b):
    return ' ' not in b

def minimax(b, depth, is_max, alpha, beta, logs):
    winner = check_winner(b)
    if winner == 'X':
        return 10 - depth
    if winner == 'O':
        return depth - 10
    if is_full(b):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'X'
                val = minimax(b, depth+1, False, alpha, beta, logs)
                b[i] = ' '
                best = max(best, val)
                alpha = max(alpha, best)
                logs.append(f"   [MAX] pos={i} score={val} alpha={alpha} beta={beta}")
                if beta <= alpha:
                    logs.append(f"   *** ALPHA CUTOFF at pos={i} ***")
                    break
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'O'
                val = minimax(b, depth+1, True, alpha, beta, logs)
                b[i] = ' '
                best = min(best, val)
                beta = min(beta, best)
                logs.append(f"   [MIN] pos={i} score={val} alpha={alpha} beta={beta}")
                if beta <= alpha:
                    logs.append(f"   *** BETA CUTOFF at pos={i} ***")
                    break
        return best

def get_best_move(player):
    logs = []
    best_val = -math.inf if player == 'X' else math.inf
    best_pos = -1

    for i in range(9):
        if board[i] == ' ':
            board[i] = player
            if player == 'X':
                val = minimax(board, 0, False, -math.inf, math.inf, logs)
                if val > best_val:
                    best_val = val
                    best_pos = i
            else:
                val = minimax(board, 0, True, -math.inf, math.inf, logs)
                if val < best_val:
                    best_val = val
                    best_pos = i
            board[i] = ' '

    print(f"\n--- Alpha-Beta Log ({'MAX' if player == 'X' else 'MIN'}) ---")
    for line in logs[:15]:
        print(line)
    if len(logs) > 15:
        print(f"   ... {len(logs)-15} more steps ...")

    return best_pos, best_val


print("=" * 35)
print("   TIC-TAC-TOE  |  MAX vs MIN")
print("   MAX plays X  |  MIN plays O")
print("=" * 35)
print("\nBoard positions:")
print(" 0 | 1 | 2 ")
print("---|---|---")
print(" 3 | 4 | 5 ")
print("---|---|---")
print(" 6 | 7 | 8 ")
print_board()

turn = 'X'
move_num = 0
max_util = 0
min_util = 0

while True:
    move_num += 1
    pos, score = get_best_move(turn)
    board[pos] = turn

    if turn == 'X':
        max_util = score
    else:
        min_util = score

    name = "MAX (X)" if turn == 'X' else "MIN (O)"
    print(f"\nMove #{move_num}: {name} -> position {pos}  |  utility = {score}")
    print(f"Scores => MAX: {max_util}   MIN: {min_util}")
    print_board()

    w = check_winner(board)
    if w:
        print(f">>> {'MAX (X)' if w == 'X' else 'MIN (O)'} WINS! <<<")
        break
    if is_full(board):
        print(">>> It's a DRAW! <<<")
        break

    turn = 'O' if turn == 'X' else 'X'

print("\n" + "=" * 35)
print(f"Final Utility -> MAX: {max_util}  |  MIN: {min_util}")
print("=" * 35)
