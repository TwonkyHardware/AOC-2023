#!/usr/bin/python3

#input_file = "./sample_input_1"

#input_file = "./reddit_input_1"
#https://old.reddit.com/r/adventofcode/comments/189q9wv/2023_day_3_another_sample_grid_to_use/

input_file = "./input_1"


# Going to be comparing lots of coordinates.  Make a function.
def is_adjacent(x1, x2):
    # Inputs are two (<int> r, <int> c) coordinate pairs

    # Check that it's not the same point
    if (x2[0] == x1[0]) and (x2[1] == x1[1]):
        return False

    in_row_range, in_column_range = False, False
    if x2[0] in [x1[0]-1, x1[0], x1[0]+1]:
        in_row_range = True
    if x2[1] in [x1[1]-1, x1[1], x1[1]+1]:
        in_column_range = True

    if in_row_range and in_column_range:
        return True
    else:
        return False


# Pull the data in and store it as a "list of lists" matrix
schematic = []
with open(input_file, "r") as data:
    lines = data.readlines()
    for line in lines:
        # Eliminate linebreak `\n` at the end of each line
        schematic.append(line[:-1])

"""
for line in schematic:
    print(line)
"""

# Find the row-column coordinates of every symbol, store as list of tuples.
# Symbols are defined as: Not a digit, not a period.
symbol_coords = []
for r,line in enumerate(schematic):
    for c,char in enumerate(line):
        if not char.isdigit() and not char == '.':
            symbol_coords.append( (int(r), int(c)) )

#print(symbol_coords)
# symbol_coords ~> [(1, 3), (3, 6), (4, 3), (5, 5), (8, 3), (8, 5)]

# Find every number and note the row-column coordinates of each of its digits.
number_coords = []
for r,line in enumerate(schematic):
    current_number = []
    current_coords = []
    for c,char in enumerate(line):
        # If we find a digit, start constructing the entry
        if char.isdigit():
            current_number.append(char)
            current_coords.append( (int(r), int(c)) )
        else:
            if current_number and current_coords:
                number_coords.append(
                    (int(''.join(current_number)), current_coords)
                )
                # Reset
                current_number = []
                current_coords = []

        # Check for end of line!  Reddit sample saved me a star here
        if c == (len(line)-1):
            if current_number and current_coords:
                number_coords.append(
                    (int(''.join(current_number)), current_coords)
                )
                # Reset
                current_number = []
                current_coords = []

"""
for tup in number_coords:
    print(tup)
"""
# number_coords ~> [(467, [(0, 0), (0, 1), (0, 2)]),
#                   (114, [(0, 5), (0, 6), (0, 7)]),
#                   (35, [(2, 2), (2, 3)]), ... ]

# Loop over all numbers. If any of its digits are adjacent to a symbol coordinate,
# add it to the list.
part_numbers = []
for num_tuple in number_coords:
    digit = num_tuple[0]
    coords = num_tuple[1]
    # If *any* digit is adjacent to *any* symbol, the number passes
    number_pass = False
    for symbol_coord in symbol_coords:
        for coord in coords:
            if is_adjacent(coord, symbol_coord):
                #print(f'{coord} and {symbol_coord} are adjacent')
                number_pass = True

    if number_pass:
        part_numbers.append(digit)

#print(part_numbers)
# part_numbers ~> [467, 35, 633, 617, 592, 755, 664, 598]

# Result:
print(sum(part_numbers))
