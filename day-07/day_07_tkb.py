def parse_file(in_filename):
# Parse input file and return a list of 2-tples (target, list_of_inputs)
    data = []

    f_in = open(in_filename)
    for L_string in f_in:
        L = L_string.strip()
        target_inputs_list = L.split(":")
        target = int(target_inputs_list[0])
        inputs = [int(x) for x in target_inputs_list[1].split()]
        data.append((target, inputs))
    return data

def calculate_result_1(in_data):
    # Sum target in rows where there is at least one way to obtain the target from the inputs
    return sum(target for (target, inputs) in in_data if (count_ways(target, inputs) > 0))

def calculate_result_2(in_data):
    return sum(target for (target, inputs) in in_data if (count_ways_2(target, inputs) > 0))

def count_ways(target, inputs):
    # Return number of ways (i.e. combinations of operators +, *) to obtain target from inputs.
    # Principle: Recursion backward from end of list of inputs.
    # Using idea that count_ways(target, [a, b, c]) = count_ways(target - c, [a, b]) + count_ways(target / c, [a, b])
    #   i.e. sum of (number of ways if operator between b and c is "+") plus (number of ways if operator between b and c is "*").

    if len(inputs) == 1:
        # Base case: if there is only one input, then it is a possible awy if and only if the input is the target number itself.
        return (target == inputs[0])
    else:
        # Recursive case
        inputs_head = inputs[0:-1]
        input_tail = inputs[-1]

        num_ways = 0
        if target >= input_tail:
            # i.e. if target *might* be input_tail + (SOME combination of the inputs_head, which is guaranteed to be > 0) 
            num_ways += count_ways(target - input_tail, inputs_head)
        if (target % input_tail) == 0:
            # i.e. if target *might* be input_tail * (SOME combination of the inputs_head, which is guaranteed to be integer) 
            num_ways += count_ways(target // input_tail, inputs_head)
        return num_ways

def count_ways_2(target, inputs):
    # Similar recursive approach to count_ways but with an extra case for the concatenation operator

    if len(inputs) == 1:
        # Base case
        return (target == inputs[0])
    else:
        # Recursive case
        inputs_head = inputs[0:-1]
        input_tail = inputs[-1]

        num_ways = 0

        if target >= input_tail:
            # i.e. if target *might* be input_tail + (SOME combination of the inputs_head, which is guaranteed to be >= 0) 
            num_ways = num_ways + count_ways_2(target - input_tail, inputs_head)
        
        if (target % input_tail) == 0:
            # i.e. if target *might* be input_tail * (SOME combination of the inputs_head, which is guaranteed to be integer) 
            num_ways = num_ways + count_ways_2(target // input_tail, inputs_head)

        if (len(str(target)) > len(str(input_tail)) and str(target).endswith(str(input_tail))):
            # i.e. if target might be concatenation of (SOME positive integer) and input_tail
            num_ways = num_ways + count_ways_2(int(str(target).removesuffix(str(input_tail))), inputs_head)
        return(num_ways)


# Test code
data_test = parse_file("day-07/input-test.txt")
result_test_exp_1 = 3749
result_test_exp_2 = 11387
result_test_actual_1 = calculate_result_1(data_test)
result_test_actual_2 = calculate_result_2(data_test)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
print("Part 2 test: %s" % check_test_2)

# Main code

in_data = parse_file("day-07/input.txt")
result = calculate_result_1(in_data)
print("Part 1 result: %s" % result)

result = calculate_result_2(in_data)
print("Part 2 result: %s" % result)
