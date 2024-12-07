from copy import deepcopy

# We encode directions as int 0-3. Below is mapping from these to coordinate steps (for row and column).
dirs = [(0, +1), (+1, 0), (0, -1), (-1, 0)]

class data:
    # Class to store the data input
    def __init__(self, grid, start_row, start_col, start_dir):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start_row = start_row
        self.start_col = start_col
        self.start_dir = start_dir

def parse_file(in_filename):
# Parse input file and return a "data" object containing the input data
    grid = []

    f_in = open(in_filename)
    for L_string in f_in:
        L = list(L_string.strip())
        grid.append(L)
        if "^" in L:
            start_row = len(grid) - 1
            start_col = L.index("^")
            start_dir = 3
            grid[start_row][start_col] = "."
    return data(grid, start_row, start_col, start_dir)

def calculate_result_1(in_data):
    (grid_visited, _) = generate_final_state(in_data)
    return sum([any(grid_visited[r][c][d] for d in range(4))
                for r in range(in_data.rows) for c in range(in_data.cols)])

def calculate_result_2(in_data):
    (grid_visited, _) = generate_final_state(in_data)

    # Generate candidates for block: the cells the guard visited, except for the starting one.
    block_cands = {(row, col) for row in range(in_data.rows) for col in range(in_data.cols)
                   if any(grid_visited[row][col]) and not(row == in_data.start_row and col == in_data.start_col)}

    # For each candidate, produce a new initial set of data adding the block, and check if it results in loop
    result = 0
    while block_cands:
        (block_row, block_col) = block_cands.pop()
        updated_grid = deepcopy(in_data.grid)
        updated_grid[block_row][block_col] = "#"
        updated_in_data = data(updated_grid, in_data.start_row, in_data.start_col, in_data.start_dir)
        (_, is_loop) = generate_final_state(updated_in_data)
        if is_loop:
            result = result + 1
    return result

def generate_final_state(in_data):
    # Based on initial state in in_data, generate and return
    #   grid_visited[row][col][dir] with "True" where guard has been
    #   is_loop which is True if the guard is in a loop

    grid_visited = [[[False for d in range(4)] for j in range(in_data.cols)] for i in range(in_data.rows)]

    row = in_data.start_row
    col = in_data.start_col
    dir = in_data.start_dir
    grid_visited[row][col][dir] = True

    while True:
        # Keep stepping until walk off grid or reach a (row, col, dir) we've been in before.
        (row, col, dir) = step(in_data, row, col, dir)
        if row is None:
            is_loop = False
            break
        if grid_visited[row][col][dir] == True:
            is_loop = True
            break
        grid_visited[row][col][dir] = True
    
    return (grid_visited, is_loop)


def step(in_data, row, col, dir):
    # Return next row, col, and direction after next step taken, based on current values and the grid in the initial state 
    row_next = row + dirs[dir][0]
    col_next = col + dirs[dir][1]
    if (row_next < 0 or row_next >= in_data.rows) or (col_next < 0 or col_next >= in_data.cols):
        return ((None, None, None))
    elif in_data.grid[row_next][col_next] == "#":
        return((row, col, (dir + 1) % 4))
    elif in_data.grid[row_next][col_next] == ".":
        return((row_next, col_next, dir))
    raise(ValueError)

# Test code
data_test = parse_file("day-06/input-test.txt")
result_test_exp_1 = 41
result_test_exp_2 = 6
result_test_actual_1 = calculate_result_1(data_test)
result_test_actual_2 = calculate_result_2(data_test)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
print("Part 2 test: %s" % check_test_2)

# Main code

in_data = parse_file("day-06/input.txt")
result = calculate_result_1(in_data)
print("Part 1 result: %s" % result)

result = calculate_result_2(in_data)
print("Part 2 result: %s" % result)
