import numpy as np

class Grid:

    def __init__(self, size=4):
        self.grid = np.zeros((size, size), dtype=int)
        self.size = size
        self.score = 0
        self.moves = 0
        self.populate(n_tiles=2)

    def shift(self, grid):

        new_grid = np.zeros((self.size, self.size)) 
        
        for i, row in enumerate(grid): 
            fill = self.size - 1
            for tile in row: 
                
                if tile: 
                    new_grid[i][fill] = tile 
                    fill -= 1
        return new_grid

    def combine(self, grid):
        for i in range(self.size): 
            for j in range(self.size - 1): 
                score = self.handle(grid, i, j)
                self.score += score
        return grid
    
    def handle(self, grid, i, j):
        score = 0
        if grid[i][j] == grid[i][j + 1] and grid[i][j]: 
            grid[i][j] *= 2
            grid[i][j + 1] = 0
            score = grid[i][j] 
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
        
        if not np.array_equal(temp, self.grid):
            self.grid = temp
            self.moves += 1
            self.populate() 
        
        score, moves = self.score, self.moves
        points, moved = score - prev_score, moves > prev_moves
        return score, moves, points, moved

    def move_left(self, grid):
        grid = np.flip(grid, 1) 
        grid = self.shift(grid) 
        grid = self.combine(grid) 
        grid = self.shift(grid) 
        grid = np.flip(grid, 1) 
        return grid

    def move_right(self, grid):
        grid = self.shift(grid) 
        grid = self.combine(grid) 
        grid = self.shift(grid) 
        return grid
    
    def move_up(self, grid):
        grid = np.rot90(grid, 1) 
        grid = np.flip(grid, 1) 
        grid = self.shift(grid) 
        grid = self.combine(grid) 
        grid = self.shift(grid) 
        grid = np.flip(grid, 1) 
        grid = np.rot90(grid, 3) 
        return grid

    def move_down(self, grid):
        grid = np.rot90(grid, 1) 
        grid = self.shift(grid) 
        grid = self.combine(grid) 
        grid = self.shift(grid) 
        grid = np.rot90(grid, 3) 
        return grid
    
    def move_horizontal(self):
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return True
        return False

    def move_vertical(self):
        for i in range(self.size - 1):
            for j in range(self.size):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return True
        return False

    def game_over(self):
        if np.any(self.grid.astype(int) == 0):
            return False
        if np.any(self.grid.astype(int) == 2048):
            return 2048
        return not self.move_horizontal() and not self.move_vertical()
        
    def populate(self, n_tiles=1):

        for _ in range(n_tiles):
            row, col = np.where(self.grid == 0) 
            index = np.random.randint(0, len(row))

            if n_tiles == 2:
                tile = 2
            else:
                tile = np.random.choice([2, 4])
            self.grid[row[index], col[index]] = tile 

    def numpy(self):
        return self.grid
        
    def __str__(self):
        return str(self.grid)

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