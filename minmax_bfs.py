import tkinter as tk
from tkinter import messagebox
from collections import deque
import time
import timeit

start_time = time.time()
# Function to check for winning combinations
def check_winner(board, player):
    win_combinations = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]],
    ]

    for combination in win_combinations:
        if combination.count(player) == 3:
            return True
    return False

# Function to check if the board is full
def is_board_full(board):
    return board.count("") == 0

# Minimax algorithm
def minimax(board, depth, maximizing_player):
    if check_winner(board, "O"):
        return 1
    elif check_winner(board, "X"):
        return -1
    elif is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = float("-inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                eval = minimax(board, depth + 1, False)
                board[i] = ""
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                eval = minimax(board, depth + 1, True)
                board[i] = ""
                min_eval = min(min_eval, eval)
        return min_eval

# Function to get available moves
def available_moves(board):
    return [i for i in range(9) if board[i] == ""]

# Breadth-first search for Tic Tac Toe
def bfs_tic_tac_toe(board):
    queue = deque([(board, 0)])

    while queue:
        board, depth = queue.popleft()

        # Check for terminal states
        if check_winner(board, "O"):
            return 1
        elif check_winner(board, "X"):
            return -1
        elif is_board_full(board):
            return 0

        moves = available_moves(board)
        for move in moves:
            new_board = board[:]
            new_board[move] = "O" if depth % 2 == 0 else "X"
            queue.append((new_board, depth + 1))

    return 0  # No result found

# AI move using Minimax with BFS
def ai_move_with_bfs(board):
    best_move = -1
    best_eval = float("-inf")
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            eval = minimax(board, 0, False)
            board[i] = ""
            if eval > best_eval:
                best_eval = eval
                best_move = i
    return best_move

# Function to handle player's move
def player_move(board, position):
    if board[position] == "":
        board[position] = "X"
        buttons[position].config(text="X")
        if check_winner(board, "X"):
            messagebox.showinfo("Tic Tac Toe", "You win!")
            reset_board()
        elif is_board_full(board):
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            reset_board()
        else:
            ai_position = ai_move_with_bfs(board)
            if ai_position != -1:
                board[ai_position] = "O"
                buttons[ai_position].config(text="O")
                if check_winner(board, "O"):
                    messagebox.showinfo("Tic Tac Toe", "You lose!")
                    reset_board()
                elif is_board_full(board):
                    messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                    reset_board()

# Function to reset the board
def reset_board():
    for button in buttons:
        button.config(text="")
    global board
    board = [""] * 9

# Initialize the board
board = [""] * 9

# Create GUI
root = tk.Tk()
root.title("Tic Tac Toe")

# Style for buttons
button_style = {
    'font': ('Arial', 20),
    'width': 4,
    'height': 2,
    'bd': 2,
}

buttons = []
for i in range(9):
    button = tk.Button(root, text="", **button_style, command=lambda pos=i: player_move(board, pos))
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(button)

def disable_buttons():
    for button in buttons:
        button.config(state=tk.DISABLED)

def enable_buttons():
    for button in buttons:
        button.config(state=tk.NORMAL)

def reset_game():
    reset_board()
    enable_buttons()
    for button in buttons:
        button.config(text="")

def handle_game_result(result):
    if result == "X":
        messagebox.showinfo("Tic Tac Toe", "You win!")
    elif result == "O":
        messagebox.showinfo("Tic Tac Toe", "You lose!")
    elif result == "Tie":
        messagebox.showinfo("Tic Tac Toe", "It's a tie!")

def check_game_state():
    if check_winner(board, "X"):
        handle_game_result("X")
        disable_buttons()
    elif check_winner(board, "O"):
        handle_game_result("O")
        disable_buttons()
    elif is_board_full(board):
        handle_game_result("Tie")
        disable_buttons()

root.protocol("WM_DELETE_WINDOW", root.quit)  # Enable closing the window

root.mainloop()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")

