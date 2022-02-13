"""
2048 Game Clone
Logan Howard
2021-12-09
"""
# Imports
import tkinter as tk
import random

# Constants

BACKGROUND_C = "#a39489"
EMPTY_TILE_C = "#c2b3a9"

TILE_C = {
    2: "#fcefe6",
    4: "#f2e8cb",
    8: "#c4b791",
    16: "#f1d185",
    32: "#bfa569",
    64: "#f0b7a4",
    128: "#568ea6",
    256: "#3e687a",
    512: "#396e85",
    1024: "#305f92",
    2048: "#f18c8e"
}

# Game class for 2048
class Game(tk.Frame):
    
    # Constructor
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        # Create a main matrix to hold all tiles
        self.main_matrix = tk.Frame(self, bg=BACKGROUND_C, bd=1, width=500, height=500)
        self.main_matrix.grid(padx=(20), pady=(60, 20))

        # Bind keys for user input
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)

        # Call methods to create and run game
        self.create_game()
        self.start_game()
        self.mainloop()

    # Function to create the game area (matrix, tiles, score)
    def create_game(self):
        # Build a matrix and fill it with tiles
        self.tiles= []
        for i in range(4):
            row = []
            for j in range(4):
                tile = tk.Frame(self.main_matrix, bg=EMPTY_TILE_C, width=100, height=100)
                tile.grid(row=i, column=j, padx=1, pady=1)  # Place tile on matrix (tiles)
                num = tk.Label(self.main_matrix, bg=EMPTY_TILE_C)   # Create num label for each tile
                num.grid(row=i, column=j)   # Place label on tile
                data = {"tile": tile, "num": num}   # Use labels to access info for future ref
                row.append(data)
            self.tiles.append(row)

        # Create score frame
        score_header = tk.Frame(self)
        score_header.place(relx=0.5, y=30, anchor="center")
        tk.Label(score_header, text="Score").grid(row=0)
        self.score_label = tk.Label(score_header, text="0")
        self.score_label.grid(row=1)

    # Function to start the game    
    def start_game(self):
        # Create an initial start matrix
        self.matrix = []
        for i in range(4):
            self.matrix.append([0] * 4)

        # Randomly choose row & col positions for the starting tiles
        row = random.randint(0, 3)
        col = random.randint(0, 3)

        # Randomly choose weather to place a 2 or 4 for each starting tile
        start_num = random.choice([2, 4])
        self.matrix[row][col] = start_num
        self.tiles[row][col]["tile"].configure(bg=TILE_C[start_num])
        self.tiles[row][col]["num"].configure(bg=TILE_C[start_num], text=str(start_num))
        
        # Keep generating tiles while the current tile is not zero
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        
        # Randomly choose weather to place a 2 or 4 for each starting tile
        start_num = random.choice([2, 4])
        self.matrix[row][col] = start_num
        self.tiles[row][col]["tile"].configure(bg=TILE_C[start_num])
        self.tiles[row][col]["num"].configure(bg=TILE_C[start_num], text=str(start_num))

        # Initialize score
        self.score = 0

    # Function to stack
    def stack(self):
        # Create a new matrix
        new_matrix = []
        for i in range(4):
            new_matrix.append([0] * 4)

        # Perform stack
        for i in range(4):
            cur = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][cur] = self.matrix[i][j]
                    cur += 1
        self.matrix = new_matrix

    # Function to combine tiles
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    # Function to reverse matrix
    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    # Function to transpose matrix
    def transpose(self):
        # Create a new matrix
        new_matrix = []
        for i in range(4):
            new_matrix.append([0] * 4)

        # Perform the transpose
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    # Function to add new tile
    def add_tile(self):
        # Get random tile pos
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])

    # Function to update game state
    def update_game(self):
        # Loop through all tiles in matrix
        for i in range(4):
            for j in range(4):
                cur = self.matrix[i][j]
                # Check current tiles value
                if cur == 0:
                    # Update current tile data
                    self.tiles[i][j]["tile"].configure(bg=EMPTY_TILE_C)
                    self.tiles[i][j]["num"].configure(bg=EMPTY_TILE_C, text="")
                else:   # Otherwise determine its value and update tile data accordingly
                    self.tiles[i][j]["tile"].configure(bg=TILE_C[cur])
                    self.tiles[i][j]["num"].configure(bg=TILE_C[cur], text=str(cur))
        self.score_label.configure(text=self.score) # Update score
        self.update_idletasks()

   
    def move_left(self, key):
        # Manipulate matrix to move left
        self.stack()
        self.combine()
        self.stack()

        # Add tile, update game, check game state
        self.add_tile()
        self.update_game()
        self.game_state()


    def move_right(self, key):
        # Manipulate matrix to move right
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        
        # Add tile, update game, check game state
        self.add_tile()
        self.update_game()
        self.game_state()


    def move_up(self, key):
        # Manipulate matrix to move up
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()

        # Add tile, update game, check game state
        self.add_tile()
        self.update_game()
        self.game_state()


    def move_down(self, key):
        # Manipulate matrix to move down
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()

        # Add tile, update game, check game state
        self.add_tile()
        self.update_game()
        self.game_state()


    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False


    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False


   
    # Function to check game state (win / lose)
    def game_state(self):
        # Check for 2048 within the matrix
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_matrix, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="You win!").pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_matrix, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label( game_over_frame, text="Game over!").pack()


def main():
    Game()


if __name__ == "__main__":
    main()