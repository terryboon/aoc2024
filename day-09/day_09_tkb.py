from collections import namedtuple
from itertools import combinations

Block = namedtuple("Block", ["value", "length"])

def parse_file(in_filename):
    grid = []
    f_in = open(in_filename)
    line = f_in.readline().strip()
    disk = []

    file_id = 0
    on_empty = False
    for c in line:
        if on_empty:
            disk.append(Block(value=None, length=int(c)))
            on_empty = False
        else:
            disk.append(Block(value = file_id, length = int(c)))
            file_id += 1
            on_empty = True
    return(disk)              


def calculate_result_1(in_disk):
    compact_disk = compactify_disk(in_disk)
    return checksum_disk(compact_disk)

def calculate_result_2(in_data):
    antinodes = set()
    for (char, antennas) in in_data.antenna_pos.items():
        for (a, b) in combinations(antennas, 2):
            antinodes.update(generate_antinodes_2(a, b, in_data.rows, in_data.cols))
    return len(antinodes)

def compactify_disk(in_disk):

    disk = in_disk[:]

    # Find first free
    free_i = 0
    while free_i < len(disk) and disk[free_i].value is not None:
        free_i += 1
    
    # Process
    while free_i < len(disk):
        #print(printable_disk(disk))
        if disk[-1].value is None or disk[-1].length == 0:
            del disk[-1]
        else:
            if disk[-1].length == disk[free_i].length:
                disk[free_i] = disk[-1]
                del disk[-1]
            elif disk[-1].length < disk[free_i].length:
                disk.insert(free_i, disk[-1])
                disk[free_i + 1] = Block(value = None, length = disk[free_i + 1].length - disk[free_i].length)
                del disk[-1]
            elif disk[-1].length > disk[free_i].length:
                disk[free_i] = Block(disk[-1].value, disk[free_i].length)
                disk[-1] = Block(value = disk[-1].value, length = disk[-1].length - disk[free_i].length)
            while free_i < len(disk) and disk[free_i].value is not None:
                free_i += 1

    return(disk)

def compactify_disk_2(in_disk):
    disk = in_disk[:]

    blocks_to_sort = [b for b in in_disk if b.value is not None]

    for b in blocks_to_sort[::-1]:
        for (i, disk_b) in enumerate(disk):
            if disk_b.value == b.value:
                break
            if disk_b.value is None and disk_b.length <= b.length:
                disk.insert(i, b)
                if disk_b.length > b.length:
                    disk[i+1] = Block(None, disk_b.length - b.length)
                
                di


def printable_disk(in_disk):
    s = ""
    for b in in_disk:
        if b.value is None:
            s = s + ("." * b.length)
        else:
            s = s + (str(b.value) * b.length)
    return s

def checksum_disk(in_disk):
    checksum = 0
    b_start = 0
    for b in in_disk:
        if b.value is not None:
            checksum += b.value * b.length * (2 * b_start + b.length - 1) // 2
        b_start += b.length
    return checksum



# Test code
data_test = parse_file("day-09/input-test.txt")
result_test_exp_1 = 1928
#result_test_exp_2 = 34
result_test_actual_1 = calculate_result_1(data_test)
#result_test_actual_2 = calculate_result_2(data_test)
check_test_1 = "OK" if result_test_exp_1 == result_test_actual_1 else "FAIL (actual: %s)" % result_test_actual_1
#check_test_2 = "OK" if result_test_exp_2 == result_test_actual_2 else "FAIL (actual: %s)" % result_test_actual_2
print("Part 1 test: %s" % check_test_1)
#print("Part 2 test: %s" % check_test_2)

# Main code

in_data = parse_file("day-09/input.txt")
result = calculate_result_1(in_data)
print("Part 1 result: %s" % result)

#result = calculate_result_2(in_data)
#print("Part 2 result: %s" % result)
