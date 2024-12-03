import re

def parse_file(in_filename):
# Parse input file and return a list of the reports (where each report is a lists of integers)

    in_file = open(in_filename)
    lines = [L for L in in_file]
    return(lines)

def calculate_result_1(lines):
    result = 0
    for line in lines:
        muls = extract_muls(line)
        result = result + sum(x * y for (x, y) in muls)
    return result

def calculate_result_2(lines):
    instructions = []
    for l in lines:
        instructions.extend(extract_instructions(l))
    result = process_instructions(instructions)
    return result

def extract_muls(s):
    muls = []
    matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', s)
    for m in matches:
        muls.append((int(m[0]), int(m[1])))
    return muls

def extract_instructions(s):
    instructions = re.findall(r'do\(\)|don\'t\(\)|mul\(\d{1,3},\d{1,3}\)', s)
    return(instructions)

def process_instructions(instructions):
    result = 0
    enabled = True

    for i in instructions:
        if i == "do()":
            enabled = True
        elif i == "don't()":
            enabled = False
        else:
            mul_match = re.match(r'mul\((\d{1,3}),(\d{1,3})\)', i)
            (x, y) = (int(mul_match.group(1)), int(mul_match.group(2)))
            if enabled:
                result = result + (x * y)
    return result



# Test code
lines_test = parse_file("day-03/input-test.txt")
lines_test_2 = parse_file("day-03/input-test-2.txt")
result_test_exp_1 = 161
result_test_exp_2 = 48
result_test_actual_1 = calculate_result_1(lines_test)
result_test_actual_2 = calculate_result_2(lines_test_2)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
print("Part 2 test: %s" % check_test_2)

# Main code

lines = parse_file("day-03/input.txt")
result = calculate_result_1(lines)
print("Part 1 result: %s" % result)

result = calculate_result_2(lines)
print("Part 2 result: %s" % result)
