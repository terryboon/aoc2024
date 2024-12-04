def parse_file(in_filename):
# Parse input file and return a list of the lines in the text file

    f_in = open(in_filename)
    grid = [L.strip() for L in f_in if L.strip()]
    return(grid)

def calculate_result_1(grid):
    target = "XMAS"
    target_rev = target[::-1]

    gridlines = generate_gridlines(grid)
    
    result = sum(line.count(target) for line in gridlines) + sum(line.count(target_rev) for line in gridlines) 

    return result

def calculate_result_2(grid):
    rows = len(grid)
    cols = len(grid[0])
    result = sum(is_x_mas(grid, row, col) for row in range(1, rows - 1) for col in range(1, cols - 1))    
    return result

def is_x_mas(grid, row, col):
    if grid[row][col] == "A":
        diag_fwd = grid[row - 1][col - 1] + grid[row + 1][col + 1]
        diag_back = grid[row - 1][col + 1] + grid[row + 1][col - 1]
        if (diag_fwd == "MS" or diag_fwd == "SM") and (diag_back == "MS" or diag_back == "SM"):
            return(True)
    return(False)


def min(x, y):
    return(x if x < y else y)

def generate_gridlines(grid):
# From grid, return a list of all lines  
    lines = []
    rows = len(grid)
    cols = len(grid[0])

    # Horizontal
    lines.extend(grid)

    # Vertical
    for col in range(cols):
        lines.append("".join([grid[row][col] for row in range(rows)]))

    # Diagonal (top-left to bottom-right)
    for start_col in range(-rows + 1, cols):
        if start_col < 0:
            chars = [grid[row][start_col + row] for row in range(-start_col, min(rows, cols - start_col))]
        else:
            chars = [grid[row][start_col + row] for row in range(0, min(rows, cols - start_col))]
        lines.append("".join(chars))

    # Diagonal (top-right to bottom-left)
    for start_col in range(0, cols + rows - 1):
        if start_col < cols:
            chars = [grid[row][start_col - row] for row in range(0, min(rows, start_col + 1))]
        else:
            chars = [grid[row][start_col - row] for row in range(start_col - cols + 1, min(rows, start_col + 1))]
        lines.append("".join(chars))

    return(lines)



# Test code
grid_test = parse_file("day-04/input-test.txt")
result_test_exp_1 = 18
result_test_exp_2 = 9
result_test_actual_1 = calculate_result_1(grid_test)
result_test_actual_2 = calculate_result_2(grid_test)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
print("Part 2 test: %s" % check_test_2)

# Main code

grid = parse_file("day-04/input.txt")
result = calculate_result_1(grid)
print("Part 1 result: %s" % result)

result = calculate_result_2(grid)
print("Part 2 result: %s" % result)
