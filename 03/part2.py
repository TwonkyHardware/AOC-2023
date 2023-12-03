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


# Find the row-column coordinates of every star `*`, store as a list of tuples.
# A star is not necessarily a gear, but we'll take care of that later.
star_coords = []
for r,line in enumerate(schematic):
    for c,char in enumerate(line):
        if char == '*':
            star_coords.append( (int(r), int(c)) )
#print(star_coords)
# star_coords ~> [(1, 3), (4, 3), (8, 5)]


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
# add it to the list of parts.  This time, retain its coordinates for checking
# against gears.
part_coords = []
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
        part_coords.append(num_tuple)

"""
for coord in part_coords:
    print(coord)
"""
# part_coords ~> [(467, [(0, 0), (0, 1), (0, 2)]),
#                 (35, [(2, 2), (2, 3)]),
#                 (633, [(2, 6), (2, 7), (2, 8)]), ... ]

# Now scan through each gear.  For each gear, check each part for adjacency to any
# part number, compiling into a dictionary.
star_layout = {}
for star_coord in star_coords:
    for part_coord in part_coords:
        digit = part_coord[0]
        digit_coords = part_coord[1]
        for digit_coord in digit_coords:
            if is_adjacent(digit_coord, star_coord):
                # The part is adjacent to the current star
                #print(f'{digit_coord} and {star_coord} are adjacent')
                if star_coord in star_layout.keys():
                    if part_coord not in star_layout[star_coord]:
                        star_layout[star_coord].append(part_coord)
                        continue
                else:
                    star_layout[star_coord] = [part_coord]

"""
for k,v in star_layout.items():
    print(f'{k}: {v}')
"""
# star_layout ~>
# { (1, 3): [(467, [(0, 0), (0, 1), (0, 2)]), (35, [(2, 2), (2, 3)])],
#   (4, 3): [(617, [(4, 0), (4, 1), (4, 2)])],
#   (8, 5): [(755, [(7, 6), (7, 7), (7, 8)]), (598, [(9, 5), (9, 6), (9, 7)])] }

# A true gear is a star that is adjacent to exactly two parts.
# Filter star_layout{} for stars that satisfy this.
# For fun, see if there are stars adjacent to more than two parts, keeping them in
# a separate dictionary.
gears = {}
odd_gears = {}
for k,v in star_layout.items():
    if len(v) == 2:
        gears[k] = v
    elif len(v) > 2:
        odd_gears[k] = v
"""
for k,v in gears.items():
    print(f'{k}: {v}')
"""
# gears ~> { (1, 3): [(467, [(0, 0), (0, 1), (0, 2)]), (35, [(2, 2), (2, 3)])],
#            (8, 5): [(755, [(7, 6), (7, 7), (7, 8)]), (598, [(9, 5), (9, 6), (9, 7)])] }

# No odd gears in the sample input, a few in the Reddit input.
# None in the Part 2 real input.
"""
for k,v in odd_gears.items():
    print(f'{k}: {v}')
"""
# odd_gears ~>
# { (7, 6): [(23, [(6, 7), (6, 8)]), (90, [(7, 4), (7, 5)]), (12, [(7, 7), (7, 8)])]
#   (10, 1): [(2, [(9, 0)]), (2, [(9, 2)]), (1, [(11, 0)]), (1, [(11, 2)])] }

# Now find gear ratios for everything in `gears{}`.
gear_ratios = [v[0][0]*v[1][0] for v in gears.values()]
#print(gear_ratios)
#print(len(gear_ratios))
# gear_ratios ~> [16345, 451490], [6084, 672]

# Result:
print(sum(gear_ratios))
# Part 2 final result: 73646890
# 324 gears
