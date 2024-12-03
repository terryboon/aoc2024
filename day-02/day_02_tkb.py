def parse_file(in_filename):
# Parse input file and return a list of the reports (where each report is a lists of integers)

    in_file = open(in_filename)

    reports = []

    for line in in_file:
        report = [int(level) for level in line.strip().split()]
        reports.append(report)

    return(reports)

def calculate_result_1(reports):
    safe_report_count = [is_report_safe(report) for report in reports].count(True)
    return safe_report_count

def calculate_result_2(reports):
    safe_with_damping_report_count = [is_report_safe_with_damping(report) for report in reports].count(True)
    return safe_with_damping_report_count

def sign(x):
# Return an int (-1, 0, +1) to indicate sign of the argument x 
    if x < 0:
        return(-1)
    elif x > 0:
        return(+1)
    elif x == 0:
        return(0)
    else:
        raise(ValueError)

def is_report_safe(report):
# Takes a report (list of integers, "levels") and returns True if it is "safe" per Part 1 definition, False otherwise
    diffs = [(level_next - level_current) for (level_next, level_current) in zip(report[1:], report[0:-1])]        
    is_diff_size_ok = all((0 <= abs(d) and abs(d) <= 3 for d in diffs))
    is_diff_sign_ok = all((sign(d) == sign(diffs[0])) for d in diffs[1:])
    return (is_diff_size_ok and is_diff_sign_ok)

def is_report_safe_with_damping(report):
# Takes a report (list of integers, "levels")
# Returns True if it is "safe" per Part 2 definition (allowing damping), False otherwise

    diffs = [(level_next - level_current) for (level_next, level_current) in zip(report[1:], report[0:-1])]        

    # Check case of no removals (damping)
    if is_report_safe(report):
        return True

    # We are in case where we have to check if a single removal can turn report into being safe

    # Create set of indexes which are candidates for removal with the "damping".
    removal_cands = set()

    # Add indexes of levels either side of a difference which is outside 0 < abs(diff) <= 3
    for (i, diff) in enumerate(diffs):
        if abs(diff) == 0 or abs(diff) > 3:
            removal_cands.add(i)
            removal_cands.add(i+1)
    
    # Add indexes of levels where the sign of the differences changes
    # i.e. given x[i], x[i+1], x[i+2], if signs of x[i+1] - x[i] and x[i+2] - x[i+1] are different (i.e. sequence "changes direction")
    # then add i, i+1, i+2 to the list of indexes.
    for (i, (d1, d2)) in enumerate(zip(diffs[:-1], diffs[1:])):
        if sign(d1) != sign (d2):
            removal_cands.add(i)
            removal_cands.add(i+1)
            removal_cands.add(i+2)

    # Work through the candidates and check if removal makes the report "safe" per Part 1 definition.
    for i in removal_cands:
        report_removed = report[:i] + report[i+1:]
        if is_report_safe(report_removed):
            return True
    
    # If none of these worked, then report can't be made safe
    return False

# Test code
reports_test = parse_file("day-02/input-test.txt")
result_test_exp_1 = 2
result_test_exp_2 = 4
result_test_actual_1 = calculate_result_1(reports_test)
result_test_actual_2 = calculate_result_2(reports_test)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
print("Part 2 test: %s" % check_test_2)

# Main code

reports = parse_file("day-02/input.txt")
result = calculate_result_1(reports)
print("Part 1 result: %s" % result)

result = calculate_result_2(reports)
print("Part 2 result: %s" % result)
