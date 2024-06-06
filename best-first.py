import tkinter as tk
from tkinter import messagebox
import random

# Function to check for a winner
def check_winner(board):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]  # Row win
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]  # Column win
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]  # Diagonal win
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]  # Diagonal win
    return None

# Function to check if the board is full
def is_board_full(board):
    for row in board:
        if "" in row:
            return False
    return True

# Function to perform the player's move
def player_move(row, col):
    global player_turn, board

    if board[row][col] == "" and not game_over:
        labels[row][col].config(text="X", fg="red")
        board[row][col] = "X"

        winner = check_winner(board)
        if winner:
            messagebox.showinfo("Tic Tac Toe", f"Player {winner} wins!")
            reset_game()
        elif is_board_full(board):
            messagebox.showinfo("Tic Tac Toe", "It's a Draw!")
            reset_game()
        else:
            player_turn = False
            ai_move()

# Function to reset the game
def reset_game():
    global player_turn, board, game_over
    player_turn = True
    game_over = False
    board = [["" for _ in range(3)] for _ in range(3)]
    for row in labels:
        for label in row:
            label.config(text="", state=tk.NORMAL)

    # Ask the player who starts the game
    result = messagebox.askquestion("Tic Tac Toe", "Do you want to start the game?")
    if result == 'yes':
        player_turn = True
    else:
        player_turn = False
        ai_move()

count = 0  # adding count

# Function to perform the AI's move
def ai_move():
    global player_turn, board, game_over

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] != "":
                global count
                count += 1

    if not any((cell != "" for row in board for cell in row) or (count == 1)):
        # AI's first move strategy
        first_move_strategy = random.choice(["random", "center"])

        if first_move_strategy == "random":
            # Randomly select a move
            row, col = random.choice([(i, j) for i in range(3) for j in range(3) if board[i][j] == ""])
        else:
            # Center move strategy
            center_cell = (1, 1)
            if board[center_cell[0]][center_cell[1]] == "":
                row, col = center_cell
            else:
                row, col = random.choice([(i, j) for i in range(3) for j in range(3) if board[i][j] == ""])

    else:
        # Use the best-first search heuristic for subsequent moves
        _, move = best_first_search(board)
        if move:
            row, col = move
        else:
            # If no winning or blocking moves, make any valid move
            empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
            row, col = random.choice(empty_cells)

    labels[row][col].config(text="O", fg="green")
    board[row][col] = "O"

    winner = check_winner(board)
    if winner:
        messagebox.showinfo("Tic Tac Toe", f"Player {winner} wins!")
        reset_game()
    elif is_board_full(board):
        messagebox.showinfo("Tic Tac Toe", "It's a Draw!")
        reset_game()
    else:
        player_turn = True

# Best-First Search heuristic
def best_first_search(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
    random.shuffle(empty_cells)  # Shuffle for randomness

    for cell in empty_cells:
        if is_winning_move(board, "O", cell):
            return float("inf"), cell
        elif is_winning_move(board, "X", cell):
            return float("-inf"), cell

    return 0, None  # No winning move found

def is_winning_move(board, player, move):
    board_copy = [row[:] for row in board]
    board_copy[move[0]][move[1]] = player
    return check_winner(board_copy) == player

# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(bg="black")

# Initialize game variables
player_turn = True
game_over = False
board = [["" for _ in range(3)] for _ in range(3)]

# Create labels for the Tic Tac Toe grid
labels = [[None, None, None] for _ in range(3)]
for i in range(3):
    for j in range(3):
        labels[i][j] = tk.Label(root, text="", font=("Helvetica", 16), width=8, height=4, relief=tk.RIDGE,
                                borderwidth=2, padx=2, pady=2, bg="black", fg="white")
        labels[i][j].grid(row=i, column=j, padx=0, pady=0)
        # Bind the click event to each label
        labels[i][j].bind("<Button-1>", lambda event, row=i, col=j: player_move(row, col))

# Create a Reset button
reset_button = tk.Button(root, text="Reset", font=("Helvetica", 16), width=8, height=2, command=reset_game, bg="yellow")
reset_button.grid(row=3, columnspan=3)

# Ask the player who starts the game
result = messagebox.askquestion("Tic Tac Toe", "Do you want to start first?")
if result == 'no':
    player_turn = False
    ai_move()

# Run the GUI main loop
root.mainloop()