import math

#CONSTANTS
INFTY = math.inf
board = ["_"] * 9

def display(board):
    for i in range(0, 3):
        r = 3 * i
        print(board[r], board[r+1], board[r+2])
    print()

def eval_pos(board, turn, ply):
    moves = list_moves(board, "X" if turn == 1 else "O")

    #Check for win condition
    winner = check_winner(board)
    if winner == "X":
        return (INFTY, ply, board) #Player X wins
    elif winner == "O":
        return (-INFTY, ply, board) #Player O wins
    
    #Check if it's a draw (no moves left and no winner)
    if len(moves) == 0:
        return (0, ply, board)

    #Minimax to find the best move
    best_move = moves[0]
    best_move_eval = -INFTY * turn
    best_ply = INFTY

    for move in moves:
        eval, next_ply, _ = eval_pos(move, -turn, ply + 1)
        
        #Update the best move based on evaluation
        if eval * turn > best_move_eval * turn or (eval == best_move_eval and next_ply < best_ply):
            best_move_eval = eval
            best_move = move
            best_ply = next_ply

    return (best_move_eval, best_ply, best_move)

def check_winner(board):
    #Check rows, columns, and diagonals
    win_patterns = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Columns
        (0, 4, 8), (2, 4, 6) # Diagonals
    ]
    for i, j, k in win_patterns:
        if board[i] == board[j] == board[k] and board[i] != "_":
            return board[i]
    return None

def list_moves(board, e):
    moves = []
    for r in range(9):
        if board[r] == "_":
            new = board.copy()
            new[r] = e
            moves.append(new)
    return moves

def game():
    display(board)
    start_mode = str(input("Would you like to go first? (Y/N)"))
    if start_mode == "N":
        _, _, best_move = eval_pos(board, -1, 0)
        board[:] = best_move
        display(board)
    elif start_mode == "Y":
        pass
    while True:
        input_move = int(input("Make your move (0-8): "))
        if input_move > 8 or input_move < 0 or board[input_move] != "_":
            print("Invalid move! Try again.")
            continue
        board[input_move] = "X"
        
        if check_winner(board) == "X":
            display(board)
            print("Congratulations! You win!")
            break
        elif "_" not in board:
            display(board)
            print("It's a draw!")
            break
        
        _, _, best_move = eval_pos(board, -1, 0)
        if best_move == board:
            print("It's a draw!")
            break
        board[:] = best_move
        display(board)

        if check_winner(board) == "O":
            print("Game over, you lose.")
            break
        elif "_" not in board:
            print("It's a draw!")
            break

game()
