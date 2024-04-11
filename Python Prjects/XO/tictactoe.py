import tkinter as tk
from tkinter import messagebox
import random

player_score = 0
computer_score = 0

def check_winner(board):
    for row in board + list(zip(*board)) + [(board[i][i] for i in range(3)), (board[i][2 - i] for i in range(3))]:
        if all(cell == 'X' for cell in row):
            return 'Player'
        elif all(cell == 'O' for cell in row):
            return 'Computer'
    return None

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def animate_button(button, relief=tk.SUNKEN, duration=50):
    initial_relief = button.cget('relief')
    steps = 10
    delay = duration // steps
    for i in range(steps):
        new_relief = relief if i % 2 == 0 else initial_relief
        button.after(delay * i, button.config, {'relief': new_relief})
    button.after(duration, button.config, {'relief': initial_relief})

def computer_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'O'
        buttons[row][col].config(text='O', fg='white', bg='#FFA07A', state='disabled')
        animate_button(buttons[row][col])
        if check_winner(board) == 'Computer':
            messagebox.showinfo("Game Over", "Computer wins! Better luck next time.", icon='warning')
            reset_board(computer=True)
        elif is_board_full(board):
            messagebox.showinfo("Game Over", "It's a tie! Try again.", icon='info')
            reset_board()

def player_move(row, col):
    if board[row][col] == ' ':
        board[row][col] = 'X'
        buttons[row][col].config(text='X', fg='white', bg='cyan', state='disabled')
        animate_button(buttons[row][col])
        if check_winner(board) == 'Player':
            messagebox.showinfo("Game Over", "Congratulations! You win!", icon='info')
            reset_board(player=True)
        elif is_board_full(board):
            messagebox.showinfo("Game Over", "It's a tie! Try again.", icon='info')
            reset_board()
        else:
            computer_move(board)

def reset_board(player=False, computer=False):
    global player_score, computer_score
    if player:
        player_score += 1
    elif computer:
        computer_score += 1
    player_score_label.config(text=f"Player: {player_score}")
    computer_score_label.config(text=f"Computer: {computer_score}")
    for i in range(3):
        for j in range(3):
            board[i][j] = ' '
            buttons[i][j].config(text='', bg='#222', state='normal', fg='white')

def create_board():
    global board
    board = [[' ']*3 for _ in range(3)]

def create_gui():
    root = tk.Tk()
    root.title("Tic Tac Toe")

    # Create main frame
    main_frame = tk.Frame(root, bg='#222')
    main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    # Create game board
    create_board()
    global buttons, player_score_label, computer_score_label
    buttons = [[tk.Button(main_frame, text='', font=('Helvetica', 20), width=6, height=3,
                          command=lambda row=i, col=j: player_move(row, col), fg='white', bg='#222')
                for j in range(3)] for i in range(3)]
    for i, row in enumerate(buttons):
        for j, button in enumerate(row):
            button.grid(row=i, column=j, padx=5, pady=5)
    
    # Create score labels
    score_frame = tk.Frame(root, bg='#222')
    score_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
    player_score_label = tk.Label(score_frame, text=f"Player: {player_score}", font=('Helvetica', 12), bg='#222', fg='white')
    player_score_label.pack(side=tk.LEFT, padx=(0, 10))
    computer_score_label = tk.Label(score_frame, text=f"Computer: {computer_score}", font=('Helvetica', 12), bg='#222', fg='white')
    computer_score_label.pack(side=tk.RIGHT, padx=(10, 0))
    
    # Create reset button
    reset_button = tk.Button(root, text='Reset', font=('Helvetica', 14), width=10, command=reset_board, bg='#222', fg='white')
    reset_button.pack(pady=(10, 0))

    root.configure(bg='#222')
    root.mainloop()

if __name__ == "__main__":
    create_gui()
