import tkinter as tk
from tkinter import messagebox
import random

# Constants for the grid size and number of mines
GRID_SIZE = 9
NUM_MINES = 10
DEBUG = 0


class Minesweeper:
    def __init__(self, master):
        # Create the main window
        self.marked_bombs = NUM_MINES
        self.master = master
        self.master.title("Minesweeper")

        # Create the grid of squares
        self.grid = []
        for row in range(GRID_SIZE):
            self.grid.append([])
            for col in range(GRID_SIZE):
                button = tk.Button(master, width=4, height=2, command=lambda row=row, col=col: self.reveal_number(row, col))
                button.bind("<3>", lambda event, row=row, col=col: self.flag(row, col))
                button.grid(row=row, column=col)
                self.grid[row].append(button)

        # Place mines randomly
        self.mines = set()
        while len(self.mines) < NUM_MINES:
            self.mines.add((random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)))

    def get_neighbors(self, list_of_coordinates):
        neighbors = []
        for (x, y) in list_of_coordinates:

            temp_x = x
            temp_y = y
            for i in range(3):
                if i == 0:
                    temp_x -= 1
                    temp_y -= 1
                    if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_SIZE and temp_y < GRID_SIZE):
                        neighbors.append((temp_x, temp_y))
                    continue

                temp_x += 1
                if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_SIZE and temp_y < GRID_SIZE):
                    neighbors.append((temp_x, temp_y))

            temp_x = x
            temp_y = y
            for i in range(3):
                if i == 0:
                    temp_x -= 1
                    if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_SIZE and temp_y < GRID_SIZE):
                        neighbors.append((temp_x, temp_y))
                    continue

                if i == 1:
                    continue

                temp_x += 2
                if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_SIZE and temp_y < GRID_SIZE):
                    neighbors.append((temp_x, temp_y))

            temp_x = x
            temp_y = y
            for i in range(3):
                if i == 0:
                    temp_x -= 1
                    temp_y += 1
                    if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_SIZE and temp_y < GRID_SIZE):
                        neighbors.append((temp_x, temp_y))
                    continue

                temp_x += 1
                if (temp_x > -1 and temp_y > -1) and (temp_x < GRID_SIZE and temp_y < GRID_SIZE):
                    neighbors.append((temp_x, temp_y))

        if DEBUG:
            print(f"Sending back: {neighbors}")

        return neighbors

    def flag(self, row, col):

        # If button is already flagged, unflag it
        if self.grid[row][col]["bg"] == "red":
            self.grid[row][col]["text"] = ""
            self.grid[row][col]["bg"] = "#f0f0f0"
            # self.grid[row][col]["state"] = "normal"
            self.marked_bombs += 1
            return

        # If the button is already revealed, do nothing
        if self.grid[row][col]["text"] != "":
            return

        # Flag the button with an X
        if self.marked_bombs > 0:
            self.grid[row][col]["text"] = "X"
            self.grid[row][col]["bg"] = "red"
            # self.grid[row][col]["state"] = "disabled"
            self.marked_bombs -= 1

        if self.check_game_complete():
            self.uncover_mines()
            messagebox.showinfo("Congrats!", "You win!")
            self.master.destroy()
            return

    def check_game_complete(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j]["state"] != "disabled" and (i, j) not in self.mines:
                    return False

        # Return true if every tile is "disabled" or a bomb
        return True

    def uncover_mines(self):
        for (x, y) in self.mines:
            self.grid[x][y]["text"] = "B"
            self.grid[x][y].configure(bg='yellow')

    # assumes it always gets an empty coord
    def flood_fill(self, row, col):
        empty_neighbors = []
        continue_flag = False

        self.grid[row][col]["text"] = " "
        self.grid[row][col].configure(bg="gray")
        self.grid[row][col]["state"] = "disabled"

        neighbors = self.get_neighbors([(row, col)])

        if DEBUG:
            print(f"neighbors of {row, col} = {neighbors}")

        # return

        for x, y in neighbors:
            if self.mines_touching([(x, y)]) != 0:
                self.reveal_number(x, y)
            elif self.grid[x][y]["state"] != "disabled":
                self.grid[x][y]["text"] = " "
                self.grid[x][y].configure(bg='#bdbdbd')
                self.grid[x][y]["state"] = "disabled"
                empty_neighbors.append((x, y))
                continue_flag = True

        if not continue_flag:
            return

        for x, y in empty_neighbors:
            self.flood_fill(x, y)

    def mines_touching(self, coord):
        # Count the number of mines adjacent to this square
        for (row, col) in coord:
            num_adjacent_mines = 0
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if (r, c) in self.mines:
                        num_adjacent_mines += 1

        return num_adjacent_mines

    def reveal_number(self, row, col):

        if self.grid[row][col]["bg"] == "red":
            return

        if (row, col) in self.mines:
            self.uncover_mines()
            messagebox.showinfo("Game Over", "You hit a mine!")
            self.master.destroy()
            return

        num_of_bombs = self.mines_touching([(row, col)])
        if num_of_bombs == 0:
            self.flood_fill(row, col)
        else:
            self.grid[row][col].configure(bg='#bdbdbd')
            self.grid[row][col]["text"] = str(num_of_bombs)
            self.grid[row][col]["state"] = "disabled"

        if self.check_game_complete():
            self.uncover_mines()
            messagebox.showinfo("Congratulations!", "You win!")
            self.master.destroy()
            return


if __name__ == '__main__':
    # Create the game and start the main loop
    root = tk.Tk()
    mine_sweeper = Minesweeper(root)
    root.mainloop()


