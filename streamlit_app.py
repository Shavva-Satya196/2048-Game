
import tkinter as tk
import random
from copy import deepcopy


def make_empty_board(size):
    return [[0 for _ in range(size)] for _ in range(size)]

def get_empty_cells(board):
    return [(r, c) for r in range(len(board)) for c in range(len(board)) if board[r][c] == 0]

def add_random_tile(board):
    new_board = deepcopy(board)
    empties = get_empty_cells(new_board)
    if not empties:
        return new_board
    r, c = random.choice(empties)
    new_board[r][c] = random.choice([2, 4])
    return new_board

def slide_and_merge_row(row):
    filtered = [num for num in row if num != 0]
    new_row = []
    score_gain = 0
    i = 0
    while i < len(filtered):
        if i + 1 < len(filtered) and filtered[i] == filtered[i + 1]:
            merged = filtered[i] * 2
            new_row.append(merged)
            score_gain += merged
            i += 2
        else:
            new_row.append(filtered[i])
            i += 1
    while len(new_row) < len(row):
        new_row.append(0)
    return new_row, score_gain

def move_left(board):
    new_board, total_gain, moved = [], 0, False
    for row in board:
        new_row, gain = slide_and_merge_row(row)
        if new_row != row:
            moved = True
        new_board.append(new_row)
        total_gain += gain
    return new_board, moved, total_gain

def move_right(board):
    reversed_board = [row[::-1] for row in board]
    moved_board, moved, gain = move_left(reversed_board)
    return [row[::-1] for row in moved_board], moved, gain

def transpose(board):
    return [list(row) for row in zip(*board)]

def move_up(board):
    transposed = transpose(board)
    moved_board, moved, gain = move_left(transposed)
    return transpose(moved_board), moved, gain

def move_down(board):
    transposed = transpose(board)
    moved_board, moved, gain = move_right(transposed)
    return transpose(moved_board), moved, gain

def has_moves(board):
    if get_empty_cells(board):
        return True
    size = len(board)
    for r in range(size):
        for c in range(size - 1):
            if board[r][c] == board[r][c + 1]:
                return True
            if board[c][r] == board[c + 1][r]:
                return True
    return False


class Game2048:
    def __init__(self, root, size=4, target=2048):
        self.root = root
        self.size = size
        self.target = target
        self.score = 0
        self.board = add_random_tile(add_random_tile(make_empty_board(size)))
        
        self.root.title("2048 Game")
        self.root.bind("<Key>", self.handle_key)

        self.frame = tk.Frame(self.root, bg="#bbada0")
        self.frame.grid()
        self.cells = [[tk.Label(self.frame, width=4, height=2, font=("Arial", 24, "bold"), 
                                bg="#cdc1b4", fg="#776e65", text="") 
                       for _ in range(size)] for _ in range(size)]
        
        for r in range(size):
            for c in range(size):
                self.cells[r][c].grid(row=r, column=c, padx=5, pady=5)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 16, "bold"))
        self.score_label.grid(pady=10)

        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 14, "bold"), command=self.restart)
        self.restart_button.grid(pady=5)

        self.update_ui()

    def restart(self):
        self.score = 0
        self.board = add_random_tile(add_random_tile(make_empty_board(self.size)))
        self.update_ui()

    def handle_key(self, event):
        key = event.keysym.lower()
        moved, gain = False, 0
        new_board = deepcopy(self.board)

        if key == "left":
            new_board, moved, gain = move_left(new_board)
        elif key == "right":
            new_board, moved, gain = move_right(new_board)
        elif key == "up":
            new_board, moved, gain = move_up(new_board)
        elif key == "down":
            new_board, moved, gain = move_down(new_board)
        else:
            return

        if moved:
            self.score += gain
            new_board = add_random_tile(new_board)
            self.board = new_board
            self.update_ui()
            if any(self.target in row for row in self.board):
                self.show_message("You Win!")
            elif not has_moves(self.board):
                self.show_message("Game Over!")

    def show_message(self, msg):
        popup = tk.Toplevel(self.root)
        popup.title(msg)
        tk.Label(popup, text=msg, font=("Arial", 20, "bold")).pack(padx=20, pady=20)
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)

    def update_ui(self):
        for r in range(self.size):
            for c in range(self.size):
                val = self.board[r][c]
                label = self.cells[r][c]
                label.config(text=str(val) if val != 0 else "", bg=self.get_color(val))
        self.score_label.config(text=f"Score: {self.score}")
        self.root.update_idletasks()

    def get_color(self, val):
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
            128: "#edcf72", 256: "#edcc61", 512: "#edc850",
            1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(val, "#3c3a32")


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root, size=4)
    root.mainloop()
