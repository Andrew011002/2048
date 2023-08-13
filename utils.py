import numpy as np

# adds a random tiles to grid, or initializes grid with starting tiles
def populate(grid, n_tiles=1):
    for _ in range(n_tiles):
        row, col = np.where(grid == 0) # empty spaces
        index = np.random.randint(0, len(row)) # random spot

        # starting tiles (always 2)
        if n_tiles == 2:
            tile = 2
        # new tiles after start (2 or 4)
        else:
            tile = np.random.choice([2, 4])

        grid[row[index], col[index]] = tile # place tile

    return grid

# moves tiles to rightmost
def shift(matrix, size=4):
        new_matrix = np.zeros((size, size)) 
        # iterate rows and tiles
        for i, row in enumerate(matrix): 
            fill = size - 1
            for tile in row: 
                # make non empty tiles right most (fill)
                if tile: 
                    new_matrix[i][fill] = tile 
                    fill -= 1

        return new_matrix

# conbines like tiles and returns the new grid with the score
def combine(matrix, size=4):
    score = 0
    for i in range(size): # iterate each row
        for j in range(size - 1): # iterate each tile
            if matrix[i][j] == matrix[i][j + 1] and matrix[i][j]: # matching tiles and not empty (combine)
                matrix[i][j] *= 2
                matrix[i][j + 1] = 0
                score += matrix[i][j] # update score

    return matrix, score

# moves tiles in grid based on direction
def move(grid, direction, size=4):

    matrix = grid

    if direction == "left":
        matrix = np.flip(matrix, 1) # reverse the matrix to get movements to the right in respect to the left
        matrix = shift(matrix, size=size) # push tiles to the rightmost
        matrix, score = combine(matrix, size=size) # combine like tiles
        matrix = shift(matrix, size=size) # push tiles to the rightmost
        matrix = np.flip(matrix, 1) # reverse the matrix back to the original orientation
    
    elif direction == "right":
        matrix = shift(matrix, size=size) # push tiles to the rightmost
        matrix, score = combine(matrix, size=size) # combine like tiles
        matrix = shift(matrix, size=size) # push tiles to the rightmost

    elif direction == "up":
        matrix = np.rot90(matrix, 1) # rotate the matrix 90 degrees counter-clockwise to get movements to the right in respect to down
        matrix = np.flip(matrix, 1) # reverse the matrix to get movements to the right in respect to the up (left)
        matrix = shift(matrix, size=size) # push tiles to the rightmost
        matrix, score = combine(matrix, size=size) # combine like tiles
        matrix = shift(matrix, size=size) # push tiles to the rightmost
        matrix = np.flip(matrix, 1) # reverse the matrix back to the original orientation
        matrix = np.rot90(matrix, 3) # rotate the matrix 270 degrees counter-clockwise to get back to the original orientation   
    
    elif direction == "down":
        matrix = np.rot90(matrix, 1) # rotate the matrix 90 degrees counter-clockwise to get movements to the right in respect to down
        matrix = shift(matrix, size=size) # push tiles to the rightmost
        matrix, score = combine(matrix, size=size) # combine like tiles
        matrix = shift(matrix, size=size) # push tiles to the rightmost
        matrix = np.rot90(matrix, 3) # rotate the matrix 270 degrees counter-clockwise to get back to the original orientation
    
    # only modify the matrix if an actual move was made instead of the function being called
    if not np.array_equal(matrix, grid):
        grid = populate(matrix)
        return grid, score, 1 # moved

    return grid, score, 0 # did not move

# indicates if a horizontal move can be made
def move_horizontal(grid, size=4):
    # iterate rows in columns
    for i in range(size):
        for j in range(size - 1):
            # if adjacent tiel along the horizontal axis is the same
            if grid[i][j] == grid[i][j + 1]:
                return True
    return False

# indicates if a vertical move can be made
def move_vertical(grid, size=4):
    # iterate each rows and columns
    for i in range(size - 1):
        for j in range(size):
            # if adjacent tile along the vertical axis is the same
            if grid[i][j] == grid[i + 1][j]:
                return True
    return False

# checks if game is over based on if moves can be made or 2048 tile reached
def game_over(grid, size=4):
    if np.any(grid == 0): # if there's any open space the game is still in place
        return False

    if np.any(grid == 2048): # player won game is over
        return True

    # if any movement in all directions is the same as the original grid, the game is over
    return not move_horizontal(grid, size=size) and not move_vertical(grid, size=size)