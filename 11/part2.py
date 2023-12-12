#!/usr/bin/python3

#input_file = "./sample_input_1"

input_file = "./input_1"

def million_rows(galaxy):
    # `galaxy` is a list of strings
    # A million rows or columns will be represented by '+' signs

    new_galaxy = []
    for row in galaxy:
        row_set = set(row)
        if '#' not in row_set:
            # Millionize the row
            new_galaxy.append(''.join(['+']*len(row)))
        else:
            new_galaxy.append(row)

    return new_galaxy

# Hubble constant
H = 1000000

# Input data is small enough to be loaded into memory.  Do that first
galaxy = []
with open(input_file, "r") as data:

    lines = data.readlines()

    for line in lines:
        # Remember to toss linebreak characters
        galaxy.append(line[:-1])

#for row in galaxy: print(row)

# Check for empty rows and double them
galaxy = million_rows(galaxy)

# Do the same for columns by transposing and re-posing
galaxy = [[row[i] for row in galaxy] for i in range(len(galaxy[0]))]
galaxy = million_rows(galaxy)
galaxy = [[row[i] for row in galaxy] for i in range(len(galaxy[0]))]

#print('')
#for row in galaxy: print(''.join(row))

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
        # This time we need to count the '+' symbols
        path = []
        x_coords = (g1[0], g2[0])
        y_coords = (g1[1], g2[1])
        for horizontal in range( min(x_coords), max(x_coords) ):
            path.append(galaxy[g1[1]][horizontal])
        for vertical in range( min(y_coords), max(y_coords) ):
            path.append(galaxy[vertical][g2[0]])

        lengths.append(path.count('.') + path.count('#') + H*path.count('+'))


print(sum(lengths))
# Sample input
# H=10: 1030
# H=100: 8410
# H=1000000: 82000210
# Gah.  Accidentally input that as the real answer.  I guess there's not a penalty

# Challenge input
# H = 1000000: 702152204842

