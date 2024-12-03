from collections import Counter

def parse_file(in_filename):
# Parse input file and return lists of integers xs (for values in first col), ys (for values in second col)

    in_file = open(in_filename)

    # Create xs as list of distances in first column, ys for second column
    xs = []
    ys = []
    for line in in_file:
        dists = line.strip().split()
        xs.append(int(dists[0]))
        ys.append(int(dists[1]))

    return((xs, ys))

def calculate_result_1(xs, ys):
    xs_sorted = sorted(xs)
    ys_sorted = sorted(ys)

    dist = sum(abs(x - y) for (x, y) in zip(xs_sorted, ys_sorted))
    return dist

def calculate_result_2(xs, ys):
    y_counter = Counter(ys)
    similarity = sum(x * y_counter[x] for x in xs)
    return similarity

# Test code
xs_test = [3, 4, 2, 1, 3, 3]
ys_test = [4, 3, 5, 3, 9, 3]
result_test_exp_1 = 11
result_test_exp_2 = 31
result_test_actual_1 = calculate_result_1(xs_test, ys_test)
result_test_actual_2 = calculate_result_2(xs_test, ys_test)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
print("Part 2 test: %s" % check_test_2)

# Main code

(xs, ys) = parse_file("day-01/input.txt")
result = calculate_result_1(xs, ys)
print("Part 1 result: %s" % result)

result = calculate_result_2(xs, ys)
print("Part 2 result: %s" % result)
