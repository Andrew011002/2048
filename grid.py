import numpy as np

class Grid:

    def __init__(self, size=4):
        self.grid = np.zeros((size, size), dtype=np.float32)
        self.size = size
        self.score = 0
        self.moves = 0
        self.populate(n_tiles=2)

    def shift(self, grid):
        new_grid = np.zeros((self.size, self.size)) 
        # iterate rows and tiles
        for i, row in enumerate(grid): 
            fill = self.size - 1
            for tile in row: 
                # make non empty tiles right most (fill)
                if tile: 
                    new_grid[i][fill] = tile 
                    fill -= 1
        return new_grid

    def combine(self, grid):
        for i in range(self.size): # iterate each row
            for j in range(self.size - 1): # iterate each tile
                score = self.handle(grid, i, j)
                self.score += score
        return grid
    
    def handle(self, grid, i, j):
        score = 0
        if grid[i][j] == grid[i][j + 1] and grid[i][j]: # matching tiles and not empty (combine)
            grid[i][j] *= 2
            grid[i][j + 1] = 0
            score = grid[i][j] # get score
        return score
        
    def move(self, direction):

        temp = self.grid
        prev_score, prev_moves = self.score, self.moves

        if direction == 'left':
            temp = self.move_left(temp)
        
        elif direction == 'right':
            temp = self.move_right(temp)

        elif direction == 'up':
            temp = self.move_up(temp)
        
        elif direction == 'down':
            temp = self.move_down(temp)
        
        # only modify the grid if an actual move was made instead of the function being called
        if not np.array_equal(temp, self.grid):
            self.grid = temp
            self.moves += 1
            self.populate() # populate if the move was made
        
        # return changes in grid (e.g. points score, if the grid moved)
        score, moves = self.score, self.moves
        points, moved = score - prev_score, moves > prev_moves
        return score, moves, points, moved

    def move_left(self, grid):
        grid = np.flip(grid, 1) # reverse the grid to get movements to the right in respect to the left
        grid = self.shift(grid) # push tiles to the rightmost
        grid = self.combine(grid) # combine like tiles
        grid = self.shift(grid) # push tiles to the rightmost
        grid = np.flip(grid, 1) # reverse the grid back to the original orientation
        return grid

    def move_right(self, grid):
        grid = self.shift(grid) # push tiles to the rightmost
        grid = self.combine(grid) # combine like tiles
        grid = self.shift(grid) # push tiles to the rightmost
        return grid
    
    def move_up(self, grid):
        grid = np.rot90(grid, 1) # rotate the grid 90 degrees counter-clockwise to get movements to the right in respect to down
        grid = np.flip(grid, 1) # reverse the grid to get movements to the right in respect to the up (left)
        grid = self.shift(grid) # push tiles to the rightmost
        grid = self.combine(grid) # combine like tiles
        grid = self.shift(grid) # push tiles to the rightmost
        grid = np.flip(grid, 1) # reverse the grid back to the original orientation
        grid = np.rot90(grid, 3) # rotate the grid 270 degrees counter-clockwise to get back to the original orientation 
        return grid

    def move_down(self, grid):
        grid = np.rot90(grid, 1) # rotate the grid 90 degrees counter-clockwise to get movements to the right in respect to down
        grid = self.shift(grid) # push tiles to the rightmost
        grid = self.combine(grid) # combine like tiles
        grid = self.shift(grid) # push tiles to the rightmost
        grid = np.rot90(grid, 3) # rotate the grid 270 degrees counter-clockwise to get back to the original orientation
        return grid
    
    def move_horizontal(self):
        # iterate rows in columns
        for i in range(self.size):
            for j in range(self.size - 1):
                # if adjacent tiel along the horizontal axis is the same
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return True
        return False

    def move_vertical(self):
        # iterate each rows and columns
        for i in range(self.size - 1):
            for j in range(self.size):
                # if adjacent tile along the vertical axis is the same
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return True
        return False

    def game_over(self):
        if np.any(self.grid.astype(int) == 0): # if there's any open space the game is still in place
            return False
        if np.any(self.grid.astype(int) == 2048):
            return True
        # if any movement in all directions is the same as the original grid, the game is over
        return not self.move_horizontal() and not self.move_vertical()
        
    # adds a random tiles to grid, or initializes grid with starting tiles
    def populate(self, n_tiles=1):

        for _ in range(n_tiles):
            row, col = np.where(self.grid == 0) # empty spaces
            index = np.random.randint(0, len(row)) # random spot

            # starting tiles (always 2)
            if n_tiles == 2:
                tile = 2
            # new tiles after start (2 or 4)
            else:
                tile = np.random.choice([2, 4])
            self.grid[row[index], col[index]] = tile # place tile

    def numpy(self):
        return self.grid
        
    # prints the grid
    def __str__(self):
        return str(self.grid.astype(int))

def main():
    grid = Grid()
    print(grid)
    print()
    score, moves, points, moved = grid.move("left")
    print(grid)
    print(f"score: {score}, moves: {moves}, points: {points}, moved: {moved}")
    score, moves, points, moved = grid.move("right")
    print(grid)
    print(f"score: {score}, moves: {moves}, points: {points}, moved: {moved}")
    score, moves, points, moved = grid.move("up")
    print(grid)
    print(f"score: {score}, moves: {moves}, points: {points}, moved: {moved}")
    score, moves, points, moved = grid.move("down")
    print(grid)
    print(f"score: {score}, moves: {moves}, points: {points}, moved: {moved}")

if __name__ == "__main__":
    main()