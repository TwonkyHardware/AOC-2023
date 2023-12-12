#!/usr/bin/python3

input_file = "./sample_input_1"
#input_file = "./sample_input_2"
#input_file = "./sample_input_3"
#input_file = "./sample_input_4"

#input_file = "./input_1"


class Coordinate():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def step(self, (dx, dy)):
        self.x = self.x + dx
        self.y = self.y + dy



# Dictionary of (x,y) steps allowed by pipe shapes
dirs = {'N': (0,+1), 'E': (+1,0), 'S': (0,-1), 'W': (-1,0)}
steps = {'|': [dirs['N'], dirs['S']],
         '-': [dirs['E'], dirs['W']],
         'L': [dirs['N'], dirs['E']],
         'J': [dirs['N'], dirs['W']],
         '7': [dirs['S'], dirs['W']],
         'F': [dirs['E'], dirs['S']],
         '.': [],
         'S': []}
edge_conditions = {'N': y>0, 'E':x_max-x>0, 'S':y_max-y>0, 'W':x>0}
# Input data is small enough to be loaded into memory.  Do that first
area = []
with open(input_file, "r") as data:

    lines = data.readlines()

    for line in lines:
        area.append(line)

# Limits of the graph: (x,y) *cannot* attain these values
max_x = len(area[0])
max_y = len(area)

loop_coords = {}
# loop_coords ~> { (x,y): {'shape': 'L', 'touch': [(w,v), (z,t)]}, ... }
# Will work in coordinate tuples (x, y)
# Now find the coordinates of S
for r,row in enumerate(area):
    for c,col in enumerate(row):
        if col == 'S':
            S_coord = (c,r)
            S = Coordinate(c,r)

loop_coords[S_coord] = {'shape': None, 'touch': []}
# Now find the four points which might connect to S
xs = S_coord[0]
ys = S_coord[1]

if ys > 0:
    N_shape = area[ys-1][xs]
    if dirs['S'] in steps[N_shape]:
        loop_coords[(xs, ys-1)] = {'shape': N_shape, 'touch': [(xs, ys)]}
        loop_coords[S_coord]['touch'].append((xs, ys-1))

if xs < max_x:
    E_shape = area[ys][xs+1]
    if dirs['W'] in steps[E_shape]:
        loop_coords[(xs+1, ys)] = {'shape': E_shape, 'touch': [(xs, ys)]}
        loop_coords[S_coord]['touch'].append((xs+1, ys))

if ys < max_y:
    S_shape = area[ys+1][xs]
    if dirs['N'] in steps[S_shape]:
        loop_coords[(xs, ys+1)] = {'shape': S_shape, 'touch': [(xs, ys)]}
        loop_coords[S_coord]['touch'].append((xs, ys+1))

if xs > 0:
    W_shape = area[ys][xs-1]
    if dirs['E'] in steps[W_shape]:
        loop_coords[(xs-1, ys)] = {'shape': W_shape, 'touch': [(xs, ys)]}
        loop_coords[S_coord]['touch'].append((xs-1, ys))


if S.y > 0:
    direction = 'S'
    new_coord = Coordinate(S.y-1, S.x)
    x = new_coord.x
    y = new_coord.y
    shape = area[y][x]
    if dirs[direction] in steps[shape]:
        loop_coords[(x,y)] = {'shape': shape, 'touch': [(xs, ys)]}



print(loop_coords)
