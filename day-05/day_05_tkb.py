from collections import defaultdict
from collections import Counter

class in_data:
    def __init__(self, rules, updates):
        self.rules = rules
        self.updates = updates

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
    # Process rules
    rules_dict = defaultdict(set)
    for (k, v) in in_data.rules:
        rules_dict[k].add(v)

    # Return the sum of the middle page numbers for each update which is OK.
    return sum(update[int((len(update) - 1)/2)] for update in in_data.updates
               if is_update_ok(rules_dict, update))

def calculate_result_2(in_data):
    # Process rules
    rules_dict = defaultdict(set)
    for (k, v) in in_data.rules:
        rules_dict[k].add(v)

    bad_updates = [update for update in in_data.updates if not(is_update_ok(rules_dict, update))]

    result = 0
    for update in bad_updates:
        # Generate subset of relevant rules i.e. those where both elements of the rule are in the update
        rules_subset = [(x, y) for (x, y) in in_data.rules if (x in update and y in update)]

        rules_subset = extract_rules(in_data.rules, update)
        rules_order = topological_sort(rules_subset)
        result = result + rules_order[int((len(rules_order) - 1)/2)]
    return result

def extract_rules(rules, update):
    # Generate subset of rules where both elements of the rule are in the update
    update_set = set(update)
    rules_subset = [(x, y) for (x, y) in rules if (x in update_set and y in update_set)]
    return rules_subset

def topological_sort(in_rules):
    rules = in_rules[:]
    L = []
    S = set()
    nodes = set()
    for (x, y) in rules:
        nodes.add(x)
        nodes.add(y)

    # Populate S
    c = Counter([y for (x, y) in rules])
    for x in nodes:
        if c[x] == 0:
            S.add(x)
    
    while S:
        n = S.pop()
        L.append(n)
        ms = [m for m in nodes if (n, m) in rules]
        for m in ms:
            rules.remove((n, m))
            edges = [(x, y) for (x, y) in rules if y == m]
            if len(edges) == 0:
                S.add(m)
    
    if len(rules) > 0:
        print("ERROR")
    else:
        return L

def is_update_ok(rules_dict, update):
    predecessors = set()
    for i in range(1, len(update)):
        #print(update)
        predecessors.add(update[i-1])
        if not(predecessors.isdisjoint(rules_dict[update[i]])):
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
