import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def display_board(self):
        for row in self.board:
            print("|".join(row))
            print("-----")

    def check_win(self, player):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False

    def mark_board(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True

class TicTacToeAI(TicTacToe):
    def __init__(self):
        super().__init__()

    def ai_make_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    score = self.minimax(self, 0, False, -float('inf'), float('inf'))
                    self.board[i][j] = ' '  # Undo the move
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        row, col = best_move
        self.mark_board(row, col, 'O')
        return row, col

    def minimax(self, game, depth, is_maximizing_player, alpha, beta):
        score = self.evaluate_state(game)
        if score != 0:
            return score
        if game.is_board_full():
            return 0
        if is_maximizing_player:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if game.board[i][j] == ' ':
                        game.board[i][j] = 'O'
                        score = self.minimax(game, depth + 1, False, alpha, beta)
                        game.board[i][j] = ' '  # Undo the move
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if game.board[i][j] == ' ':
                        game.board[i][j] = 'X'
                        score = self.minimax(game, depth + 1, True, alpha, beta)
                        game.board[i][j] = ' '  # Undo the move
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def evaluate_state(self, game):
        if game.check_win('O'):
            return 10
        elif game.check_win('X'):
            return -10
        else:
            return 0

class LevelSelection:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe - Level Selection")
        self.window.geometry("300x150")  # Set the window size (width x height)
        self.label = tk.Label(self.window, text="Choose the level:")
        self.label.pack()
        self.button_user_first = tk.Button(self.window, text="User First", command=self.user_first)
        self.button_user_first.pack(pady=5)  # Add vertical space between buttons
        self.button_ai_first = tk.Button(self.window, text="AI First", command=self.ai_first)
        self.button_ai_first.pack(pady=10)
        self.level = None

    def user_first(self):
        self.level = 1
        self.window.quit()

    def ai_first(self):
        self.level = 2
        self.window.quit()

    def run(self):
        self.window.mainloop()


class TicTacToeGUI:
    def __init__(self, level):
        self.game = TicTacToeAI()
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.buttons = [[None, None, None] for _ in range(3)]
        self.create_grid_buttons()
        self.current_player = 'X' if level == 1 else 'O'
        self.game_over = False
        if self.current_player == 'O':  # AI's turn
            row, col = self.game.ai_make_move()
            self.buttons[row][col].config(text='O')
            self.current_player = 'X'

    def create_grid_buttons(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.window, text='', font=('Arial', 20), width=5, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j, sticky="nsew")
                self.buttons[i][j] = button

    def on_button_click(self, row, col):
        if not self.game_over and self.game.mark_board(row, col, self.current_player):
            self.buttons[row][col].config(text=self.current_player)
            if self.game.check_win(self.current_player):
                if self.current_player == 'X':
                    messagebox.showinfo("Tic Tac Toe", "You win!")
                elif self.current_player == 'O':
                    messagebox.showinfo("Tic Tac Toe", "AI wins!")
                self.game_over = True
            elif self.game.is_board_full():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.game_over = True
            else:
                # AI's turn
                self.current_player = 'O'
                row, col = self.game.ai_make_move()
                self.buttons[row][col].config(text='O')
                if self.game.check_win('O'):
                    messagebox.showinfo("Tic Tac Toe", "AI wins!")
                    self.game_over = True
                elif self.game.is_board_full():  # Check for a draw after the AI's move
                    messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                    self.game_over = True
                self.current_player = 'X'  # Switch back to human player

            if self.game_over:
                self.window.quit()

    def run(self):
        self.window.mainloop()


# Create an instance of LevelSelection to get the user's choice
level_selector = LevelSelection()
level_selector.run()
# Start the Tic Tac Toe game with the selected level
chosen_level = level_selector.level
if chosen_level is not None:
    tictactoe_gui = TicTacToeGUI(chosen_level)
    tictactoe_gui.run()
