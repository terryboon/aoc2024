from collections import defaultdict
from itertools import combinations

class data:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

        antenna_pos = defaultdict(list)
        for (row_index, row) in enumerate(grid):
            for (col_index, ch) in enumerate(row):
                if ch.isalnum():
                    antenna_pos[ch].append((row_index, col_index))
        self.antenna_pos = antenna_pos

def parse_file(in_filename):
    grid = []
    f_in = open(in_filename)
    for L_string in f_in:
        L = list(L_string.strip())
        if L:
            grid.append(L)
    return data(grid)

def calculate_result_1(in_data):
    antinodes = set()
    for (char, antennas) in in_data.antenna_pos.items():
        for (a, b) in combinations(antennas, 2):
            antinodes.update(generate_antinodes(a, b, in_data.rows, in_data.cols))
    return len(antinodes)

def calculate_result_2(in_data):
    antinodes = set()
    for (char, antennas) in in_data.antenna_pos.items():
        for (a, b) in combinations(antennas, 2):
            antinodes.update(generate_antinodes_2(a, b, in_data.rows, in_data.cols))
    return len(antinodes)

def generate_antinodes(a, b, rows, cols):
    # Return list of antinodes produced by a and b, where each of those is a 2-tuple, for part 1
    d_row = b[0] - a[0]
    d_col = b[1] - a[1]

    antinode_cands = [(a[0] - d_row, a[1] - d_col),
                       (b[0] + d_row, b[1] + d_col)]
    return([cand for cand in antinode_cands if 0 <= cand[0] < rows and 0 <= cand[1] < cols ])

def generate_antinodes_2(a, b, rows, cols):
    # Return list of antinodes produced by a and b, where each of those is a 2-tuple, for part 2
    antinodes = set([a, b])
    
    d_row = b[0] - a[0]
    d_col = b[1] - a[1]

    (row, col) = a
    while True:
        (row, col) = (row - d_row, col - d_col)
        if 0 <= row < rows and 0 <= col < cols:
            antinodes.add((row, col))
        else:
            break

    (row, col) = b
    while True:
        (row, col) = (row + d_row, col + d_col)
        if 0 <= row < rows and 0 <= col < cols:
            antinodes.add((row, col))
        else:
            break

    return antinodes



# Test code
data_test = parse_file("day-08/input-test.txt")
result_test_exp_1 = 14
result_test_exp_2 = 34
result_test_actual_1 = calculate_result_1(data_test)
result_test_actual_2 = calculate_result_2(data_test)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
print("Part 2 test: %s" % check_test_2)

# Main code

in_data = parse_file("day-08/input.txt")
result = calculate_result_1(in_data)
print("Part 1 result: %s" % result)

result = calculate_result_2(in_data)
print("Part 2 result: %s" % result)
