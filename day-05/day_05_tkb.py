from collections import defaultdict

class in_data:
    def __init__(self, rules, updates):
        self.rules = rules      # list of ordered pairs, one for each rule provided
        self.updates = updates  # list of list of ints (page numbers)

        # Generate self.rules_dict (do it here for efficiency)
        # mapping each rule element to a set of elements of its successors
        self.rules_successors = defaultdict(set)
        for (k, v) in rules:
            self.rules_successors[k].add(v)


def parse_file(in_filename):
# Parse input file and return an in_data object containing the rules and the updates

    rules = []
    updates = []

    f_in = open(in_filename)
    for L in f_in:
        L_str = L.strip()
        if "|" in L_str:
            L_split = L_str.split("|")
            rules.append((int(L_split[0]), int(L_split[1])))
        elif L_str:
            L_split = L_str.split(",")
            updates.append([int(x) for x in L_split])

    return(in_data(rules, updates))

def calculate_result_1(in_data):
    # Return the sum of the middle page numbers for each update which is OK.
    return sum(update[int((len(update) - 1)/2)] 
               for update in in_data.updates
               if is_update_ok(in_data, update))

def calculate_result_2(in_data):

    bad_updates = [update for update in in_data.updates if not(is_update_ok(in_data, update))]

    result = 0
    for update in bad_updates:
        # Generate list of relevant rules i.e. those where both elements of the rule are in the update
        update_rules = [(x, y) for (x, y) in in_data.rules if (x in update and y in update)]
        sorted_update = topological_sort(update_rules)
        result = result + sorted_update[(len(sorted_update) - 1)//2]
    return result

def topological_sort(in_rules):
    # Given list of ordered pairs for rules,
    # return a list of nodes which is consistent with the ordering defined by the rules
    # using topological sort.
    rules = in_rules[:]
    sorted_list = []
    unprocessed_minimal_nodes = set()
    nodes = set()
    for (x, y) in rules:
        nodes.add(x)
        nodes.add(y)

    # Populate unprocessed_minimal_nodes (S)
    unprocessed_minimal_nodes = nodes.copy()
    for (x, y) in rules:
        unprocessed_minimal_nodes.discard(y)

    while unprocessed_minimal_nodes:
        n = unprocessed_minimal_nodes.pop()
        sorted_list.append(n)
        n_successors = [m for m in nodes if (n, m) in rules]
        for n_succ in n_successors:
            rules.remove((n, n_succ))
            edges_to_n_succ = [(x, y) for (x, y) in rules if y == n_succ]
            if len(edges_to_n_succ) == 0:
                unprocessed_minimal_nodes.add(n_succ)
    
    if len(rules) > 0:
        raise(ValueError)   # Indicates loop
    else:
        return sorted_list

def is_update_ok(in_data, update):
    # Return whether the update is OK given the rules in in_data
    update_predecessors = set()
    for i in range(1, len(update)):
        update_predecessors.add(update[i-1])
        if not(update_predecessors.isdisjoint(in_data.rules_successors[update[i]])):
            return False
    return True

# Test code
data_test = parse_file("day-05/input-test.txt")
result_test_exp_1 = 143
result_test_exp_2 = 123
result_test_actual_1 = calculate_result_1(data_test)
result_test_actual_2 = calculate_result_2(data_test)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
print("Part 2 test: %s" % check_test_2)

# Main code

data = parse_file("day-05/input.txt")
result = calculate_result_1(data)
print("Part 1 result: %s" % result)

result = calculate_result_2(data)
print("Part 2 result: %s" % result)
