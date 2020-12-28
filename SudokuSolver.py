# Functions and a program that solves any sudoku puzzle
import math

# Constants
X = 'X'
GRID_EASY = [[8, 0, 0, 0, 9, 4, 0, 7, 5],
             [0, 7, 2, 0, 0, 3, 9, 0, 8],
             [0, 0, 9, 8, 7, 2, 6, 3, 0],
             [0, 9, 0, 0, 0, 0, 7, 0, 0],
             [1, 0, 7, 4, 6, 0, 0, 2, 0],
             [0, 0, 0, 7, 0, 0, 1, 0, 0],
             [4, 0, 5, 0, 0, 0, 3, 8, 7],
             [0, 0, 0, 1, 5, 8, 4, 0, 2],
             [0, 0, 0, 0, 0, 7, 0, 1, 6]]
LEN_GRID = 9
BOX_BOUND = [[0, 3], [3, 6], [6, 9]]

# Functions
def which_box(position: list) -> list:
    """Return the box bounds of the position in format
    [range_row, range_col]

    >>> which_box([0, 3])
    [range(0, 3), range(3, 6)]
    >>> which_box([7, 7])
    [range(6, 9), range(6, 9)]
    """

    i_row = position[0]
    i_col = position[1]
    out_list = ['range_row', 'range_col']

    for item in BOX_BOUND:
        i_row_lb = item[0]
        i_row_ub = item[1]
        if i_row_lb <= i_row < i_row_ub:
            out_list[0] = range(i_row_lb, i_row_ub)
    for item in BOX_BOUND:
        i_col_lb = item[0]
        i_col_ub = item[1]
        if i_col_lb <= i_col < i_col_ub:
            out_list[1] = range(i_col_lb, i_col_ub)
    return out_list
            
def check_row(grid: list, 
              position: list, value: object) -> bool:
    """Return True if the value does not appear in the row of
    the position and return False if the value appears in the
    row of the position.

    >>> check_row(GRID_EASY, [0, 1], 2)
    True
    >>> check_row(GRID_EASY, [0, 1], 4)
    False
    """

    i_row = position[0]
    i_col = position[1]
    
    for i in range(LEN_GRID):
        if grid[i_row][i] == value and i != i_col:
            return False
    return True

def check_col(grid: list, 
              position: list, value: object) -> bool:
    """Return True if the value does not appear in the column of
    the position and return False if the value appears in the
    column of the position.

    >>> check_col(GRID_EASY, [0, 1], 2)
    True
    >>> check_col(GRID_EASY, [0, 1], 7)
    False
    """

    i_row = position[0]
    i_col = position[1]

    for i in range(LEN_GRID):
        if grid[i][i_col] == value and i != i_row:
            return False
    return True

def check_box(grid: list, position: list, value: int) -> bool:
    """Return True if the value does not appear in the box of 
    the position and return False if the value appears in the 
    box of the position.

    >>> check_box(GRID_EASY, [0, 1], 4)
    True
    >>> check_box(GRID_EASY, [0, 1], 2)
    False
    """

    box_range = which_box(position)
    i_row = position[0]
    i_col = position[1]

    for row in box_range[0]:
        for col in box_range[1]:
            if grid[row][col] == value\
            and not (row == i_row and col == i_col):
                return False
    return True
    
def check_all(grid: list, position: list, value: int) -> bool:
    """Return True if the position in grid can take value as a
    and False if the position in grid cannot take value.

    >>> check_all(GRID_EASY, [0, 0], 1)
    False
    >>> check_all(GRID_EASY, [0, 2], 1)
    True
    >>> check_all(GRID_EASY, [0, 2], 3)
    True
    """

    checked_row = check_row(grid, position, value)
    checked_col = check_col(grid, position, value)
    checked_box = check_box(grid, position, value)

    return checked_row and checked_col and checked_box

def valid(grid: list, value: int) -> list:
    """Return a new list grid that replaces all possible
    positions of value with X. 

    >>> [[8, 'X', 'X', 0, 9, 4, 0, 7, 5],\
         [0, 7, 2, 0, 'X', 3, 9, 0, 8],\
         [0, 'X', 9, 8, 7, 2, 6, 3, 'X'],\
         [0, 9, 0, 0, 'X', 'X', 7, 0, 0],\
         [1, 0, 7, 4, 6, 0, 0, 2, 0],\
         [0, 0, 0, 7, 0, 0, 1, 0, 0],\
         [4, 'X', 5, 0, 0, 0, 3, 8, 7],\
         [0, 0, 0, 1, 5, 8, 4, 0, 2],\
         [0, 0, 0, 0, 0, 7, 0, 1, 6]] == valid(GRID_EASY, 1)
    True
    """

    # Create a true shallow copy of the original list
    # This is necessary as the nested lists are not shallow
    out_list = []
    for row in grid.copy():
        out_list.append(row.copy())

    for i_row in range(LEN_GRID):
        for i_col in range(LEN_GRID):
            if out_list[i_row][i_col] == 0 \
            and check_all(out_list, [i_row, i_col], value):
                out_list[i_row][i_col] = X
    return out_list
    
def algorithm_only_choice(grid: list, 
                      grid_valid: list, value: int) -> list:
    """Return grid as solved by 'only choice' deduction using
    grid_valid for a particular value.

    >>> algorithm_only_choice(GRID_EASY, valid(GRID_EASY, 1), 1)
    >>> [[8, 0, 1, 0, 9, 4, 0, 7, 5],
         [0, 7, 2, 0, 1, 3, 9, 0, 8],
         [0, 0, 9, 8, 7, 2, 6, 3, 1],
         [0, 9, 0, 0, 0, 1, 7, 0, 0],
         [1, 0, 7, 4, 6, 0, 0, 2, 0],
         [0, 0, 0, 7, 0, 0, 1, 0, 0],
         [4, 1, 5, 0, 0, 0, 3, 8, 7],
         [0, 0, 0, 1, 5, 8, 4, 0, 2],
         [0, 0, 0, 0, 0, 7, 0, 1, 6]] == GRID_EASY
    True
    """

    for i_row in range(LEN_GRID):
        for i_col in range(LEN_GRID):
            if grid_valid[i_row][i_col] == X:
                if check_row(grid_valid, [i_row, i_col], X)\
                or check_col(grid_valid, [i_row, i_col], X)\
                or check_box(grid_valid, [i_row, i_col], X):
                    grid[i_row][i_col] = value

def solve_easy(grid: list) -> list:
    """Return a solved sudoku grid. The solving process relies 
    solely on my 'only choice' algorithm.

    >>> solve_easy(GRID_EASY)
    [[8, 3, 1, 6, 9, 4, 2, 7, 5], 
     [6, 7, 2, 5, 1, 3, 9, 4, 8], 
     [5, 4, 9, 8, 7, 2, 6, 3, 1], 
     [3, 9, 6, 2, 8, 1, 7, 5, 4], 
     [1, 5, 7, 4, 6, 9, 8, 2, 3], 
     [2, 8, 4, 7, 3, 5, 1, 6, 9], 
     [4, 1, 5, 9, 2, 6, 3, 8, 7], 
     [7, 6, 3, 1, 5, 8, 4, 9, 2], 
     [9, 2, 8, 3, 4, 7, 5, 1, 6]]
    >>> [[8, 3, 1, 6, 9, 4, 2, 7, 5], 
         [6, 7, 2, 5, 1, 3, 9, 4, 8], 
         [5, 4, 9, 8, 7, 2, 6, 3, 1], 
         [3, 9, 6, 2, 8, 1, 7, 5, 4], 
         [1, 5, 7, 4, 6, 9, 8, 2, 3], 
         [2, 8, 4, 7, 3, 5, 1, 6, 9], 
         [4, 1, 5, 9, 2, 6, 3, 8, 7], 
         [7, 6, 3, 1, 5, 8, 4, 9, 2], 
         [9, 2, 8, 3, 4, 7, 5, 1, 6]] == GRID_EASY
    True
    """

    for row in grid:
        while 0 in row:
            for n in range(0, 10):
                algorithm_only_choice(grid, 
                                  valid(grid, n), n)
    return grid
