#!/usr/bin/python3

#input_file = "./sample_input_1"

input_file = "./input_1"

def double_rows(galaxy):
    # `galaxy` is a list of strings

    new_galaxy = []
    for row in galaxy:
        row_set = set(row)
        if (len(row_set) == 1) and ('.' in row_set):
            # Double-up on the next row
            new_galaxy.append(row)

        new_galaxy.append(row)

    return new_galaxy


# Input data is small enough to be loaded into memory.  Do that first
galaxy = []
with open(input_file, "r") as data:

    lines = data.readlines()

    for line in lines:
        # Remember to toss linebreak characters
        galaxy.append(line[:-1])

#for row in galaxy: print(row)

# Check for empty rows and double them
galaxy = double_rows(galaxy)

# Do the same for columns by transposing and re-posing
galaxy = [[row[i] for row in galaxy] for i in range(len(galaxy[0]))]
galaxy = double_rows(galaxy)
galaxy = [[row[i] for row in galaxy] for i in range(len(galaxy[0]))]


# Get a list of galaxy coordinates
g_coords = []
for y,row in enumerate(galaxy):
    for x,col in enumerate(row):
        if col == '#':
            g_coords.append( (x,y) )

# Now calculate lengths
lengths = []
while g_coords:
    g1 = g_coords.pop(0)
    for g2 in g_coords:
        lengths.append( abs(g2[0] - g1[0]) + abs(g2[1] - g1[1]) )

print(sum(lengths))
# = 9609130

