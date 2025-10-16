import tkinter as tk
from tkinter import messagebox
import random
from functools import reduce
from typing import List, Tuple, Optional, Callable

class Game2048:
    def __init__(self, size: int = 4):
        self.size = size
        self.score = 0
        self.game_over = False
        self.won = False
        self.board = self.initialize_board()
        self.add_random_tile()
        self.add_random_tile()
    
    def initialize_board(self) -> List[List[int]]:
        """Initialize an empty game board"""
        return [[0 for _ in range(self.size)] for _ in range(self.size)]
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get all empty cell coordinates using functional programming"""
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
    
    def add_random_tile(self) -> bool:
        """Add a random tile (2 or 4) to an empty cell"""
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return False
        
        i, j = random.choice(empty_cells)
        self.board[i][j] = 2 if random.random() < 0.9 else 4
        return True
    
    def compress_row(self, row: List[int]) -> List[int]:
        """Compress row by moving all non-zero elements to the left"""
        non_zero = list(filter(lambda x: x != 0, row))
        return non_zero + [0] * (len(row) - len(non_zero))
    
    def merge_row(self, row: List[int]) -> Tuple[List[int], int]:
        """Merge adjacent equal tiles in a row and return merged row with score"""
        if len(row) <= 1:
            return (row, 0)
        
        def merge_helper(acc: Tuple[List[int], int, int], current: int) -> Tuple[List[int], int, int]:
            result, score, prev = acc
            
            if prev == 0:
                return (result, score, current)
            elif prev == current:
                new_value = prev * 2
                return (result + [new_value], score + new_value, 0)
            else:
                return (result + [prev], score, current)
        
        compressed = self.compress_row(row)
        initial = ([], 0, compressed[0]) if compressed else ([], 0, 0)
        
        result, score, remaining = reduce(merge_helper, compressed[1:], initial)
        
        if remaining != 0:
            result.append(remaining)
        
        # Pad with zeros
        final_result = result + [0] * (len(row) - len(result))
        return (final_result, score)
    
    def move_left(self) -> bool:
        """Move tiles left and return True if board changed"""
        new_board = []
        total_score = 0
        changed = False
        
        for row in self.board:
            new_row, score = self.merge_row(row)
            new_board.append(new_row)
            total_score += score
            
            if row != new_row:
                changed = True
        
        self.board = new_board
        self.score += total_score
        return changed
    
    def move_right(self) -> bool:
        """Move tiles right by reversing, moving left, then reversing back"""
        reversed_board = [list(reversed(row)) for row in self.board]
        self.board = reversed_board
        changed = self.move_left()
        self.board = [list(reversed(row)) for row in self.board]
        return changed
    
    def move_up(self) -> bool:
        """Move tiles up by transposing, moving left, then transposing back"""
        transposed = list(map(list, zip(*self.board)))
        self.board = transposed
        changed = self.move_left()
        self.board = list(map(list, zip(*self.board)))
        return changed
    
    def move_down(self) -> bool:
        """Move tiles down by transposing, moving right, then transposing back"""
        transposed = list(map(list, zip(*self.board)))
        self.board = transposed
        changed = self.move_right()
        self.board = list(map(list, zip(*self.board)))
        return changed
    
    def can_move(self) -> bool:
        """Check if any moves are possible"""
        # Check for empty cells
        if any(0 in row for row in self.board):
            return True
        
        # Check for possible merges
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.board[i][j] == self.board[i][j + 1]:
                    return True
        
        for i in range(self.size - 1):
            for j in range(self.size):
                if self.board[i][j] == self.board[i + 1][j]:
                    return True
        
        return False
    
    def has_won(self) -> bool:
        """Check if player has reached 2048"""
        return any(any(cell >= 2048 for cell in row) for row in self.board)
    
    def make_move(self, direction: str) -> bool:
        """Make a move in the given direction"""
        if self.game_over:
            return False
        
        move_functions = {
            'left': self.move_left,
            'right': self.move_right,
            'up': self.move_up,
            'down': self.move_down
        }
        
        if direction in move_functions:
            changed = move_functions[direction]()
            
            if changed:
                self.add_random_tile()
                self.won = self.has_won()
                self.game_over = not self.can_move()
            
            return changed
        return False

class GameGUI:
    def __init__(self, size: int = 4):
        self.size = size
        self.game = Game2048(size)
        
        # Colors for different tile values
        self.tile_colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
            4096: "#3c3a32", 8192: "#3c3a32"
        }
        
        self.text_colors = {
            2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
            32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
            512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2", 4096: "#f9f6f2",
            8192: "#f9f6f2"
        }
        
        self.setup_gui()
    
    def setup_gui(self):
        """Initialize the GUI components"""
        self.root = tk.Tk()
        self.root.title("2048 Game")
        self.root.resizable(False, False)
        
        # Bind keyboard events
        self.root.bind('<Key>', self.handle_keypress)
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg="#bbada0", padx=10, pady=10)
        main_frame.pack()
        
        # Score display
        score_frame = tk.Frame(main_frame, bg="#bbada0")
        score_frame.pack(pady=(0, 10))
        
        tk.Label(score_frame, text="Score:", font=("Arial", 16, "bold"), 
                bg="#bbada0", fg="#eee4da").pack(side=tk.LEFT)
        self.score_label = tk.Label(score_frame, text="0", font=("Arial", 16, "bold"), 
                                   bg="#bbada0", fg="white")
        self.score_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Restart button
        restart_btn = tk.Button(score_frame, text="Restart", font=("Arial", 12, "bold"),
                               command=self.restart_game, bg="#8f7a66", fg="white",
                               relief="flat", padx=20)
        restart_btn.pack(side=tk.RIGHT)
        
        # Game board
        self.board_frame = tk.Frame(main_frame, bg="#bbada0")
        self.board_frame.pack()
        
        self.tiles = []
        self.create_board()
        
        # Instructions
        instructions = tk.Label(main_frame, text="Use arrow keys to move tiles", 
                               font=("Arial", 10), bg="#bbada0", fg="#eee4da")
        instructions.pack(pady=(10, 0))
        
        self.update_display()
    
    def create_board(self):
        """Create the game board GUI"""
        for i in range(self.size):
            row = []
            for j in range(self.size):
                tile_frame = tk.Frame(self.board_frame, width=80, height=80, 
                                     bg="#cdc1b4", relief="raised", borderwidth=3)
                tile_frame.grid(row=i, column=j, padx=5, pady=5)
                tile_frame.pack_propagate(False)
                
                label = tk.Label(tile_frame, text="", font=("Arial", 20, "bold"), 
                                justify="center", bg="#cdc1b4")
                label.pack(expand=True, fill="both")
                row.append(label)
            self.tiles.append(row)
    
    def get_tile_color(self, value: int) -> str:
        """Get background color for a tile value"""
        return self.tile_colors.get(value, "#3c3a32")
    
    def get_text_color(self, value: int) -> str:
        """Get text color for a tile value"""
        return self.text_colors.get(value, "#f9f6f2")
    
    def update_display(self):
        """Update the GUI to reflect current game state"""
        self.score_label.config(text=str(self.game.score))
        
        for i in range(self.size):
            for j in range(self.size):
                value = self.game.board[i][j]
                tile = self.tiles[i][j]
                
                if value == 0:
                    tile.config(text="", bg="#cdc1b4")
                else:
                    tile.config(text=str(value), 
                               bg=self.get_tile_color(value),
                               fg=self.get_text_color(value))
        
        # Check game status
        if self.game.won:
            messagebox.showinfo("Congratulations!", "You reached 2048!")
        elif self.game.game_over:
            messagebox.showinfo("Game Over", "No more moves possible!")
    
    def handle_keypress(self, event):
        """Handle keyboard input for moves"""
        key_mappings = {
            'Left': 'left',
            'Right': 'right', 
            'Up': 'up',
            'Down': 'down'
        }
        
        if event.keysym in key_mappings:
            self.game.make_move(key_mappings[event.keysym])
            self.update_display()
    
    def restart_game(self):
        """Restart the game with a new board"""
        self.game = Game2048(self.size)
        self.update_display()
    
    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()

def main():
    """Main function to start the game"""
    game_gui = GameGUI(size=4)
    game_gui.run()

if __name__ == "__main__":
    main()
