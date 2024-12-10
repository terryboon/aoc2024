from collections import namedtuple
from itertools import combinations

Data = namedtuple("Data", field_names=["grid", "rows", "cols", "level_nodes", "adjacent_nodes"])

def parse_file(in_filename):
    grid = []
    f_in = open(in_filename)
    for line in f_in:
        line = line.strip()
        if line:
            grid.append([int(level) for level in list(line)])
    rows = len(grid)
    cols = len(grid[0])

    level_nodes = {level: set() for level in range(0, 10)}
    for row in range(rows):
        for col in range(cols):
            level_nodes[grid[row][col]].add((row, col))

    adjacent_nodes = dict()
    for row in range(rows):
        for col in range(cols):
            adjacent_nodes[(row, col)] = set()
            level = grid[row][col]
            for (row_step, col_step) in step_cells(row, col, rows, cols):
                #print("%s, %s" % (row_step, col_step))
                if grid[row_step][col_step] == level + 1:
                    adjacent_nodes[(row, col)].add((row_step, col_step))
    return Data(grid, rows, cols, level_nodes, adjacent_nodes)

def step_cells(row, col, rows, cols):
    result = []
    if row > 0:
        result.append((row - 1, col))
    if row < rows - 1:
        result.append((row + 1, col))
    if col > 0:
        result.append((row, col - 1))
    if col < cols - 1:
        result.append((row, col + 1))
    return result

def calculate_result_1(in_data):

    score = 0
    for trailhead in in_data.level_nodes[0]:
        reachables = set([trailhead])

        for level in range(1, 10):
            new_reachables = set()
            for node in reachables:
                new_reachables.update(in_data.adjacent_nodes[node])
            reachables = new_reachables

        score = score + len(reachables)

    return score

def calculate_result_2(in_data):
    paths_from_node = dict()

    # Populate paths_from_node for level 9
    paths_from_node.update((node, 1) for node in in_data.level_nodes[9])

    # Work backwards
    for level in range(8, -1, -1):
        for x in in_data.level_nodes[level]:
            paths_from_node[x] = sum(paths_from_node[y] for y in in_data.adjacent_nodes[x])
    
    return sum(paths_from_node[x] for x in in_data.level_nodes[0])


# Test code
data_test = parse_file("day-10/input-test.txt")
result_test_exp_1 = 36
result_test_exp_2 = 81
result_test_actual_1 = calculate_result_1(data_test)
result_test_actual_2 = calculate_result_2(data_test)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
print("Part 2 test: %s" % check_test_2)

# Main code

in_data = parse_file("day-10/input.txt")
result = calculate_result_1(in_data)
print("Part 1 result: %s" % result)

result = calculate_result_2(in_data)
print("Part 2 result: %s" % result)
