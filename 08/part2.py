#!/usr/bin/python3

"""
Spent too much time doing the wrong thing on Part 1, couldn't finish
this one in time.  No stars.
"""

input_file = "./sample_input_1"
#input_file = "./sample_input_2"

#input_file = "./input_1"

def increment_to_z(path_dict, nodes, directions):
    # path_dict ~> {'start':'JHA', 'current':'JFL', 'steps':1}

    current_node = path_dict['current']
    # Trim `directions` by the number of steps already taken 
    current_directions = directions[path_dict['steps']:]

    steps = 0
    lost = True
    limit = 1000
    loop = 0
    while lost:

        if loop == limit:
            # Loops through the graph are possible.  In particular,
            # there are dead-end nodes like
            #   EEE = (EEE, EEE),
            # which are automatic loops if entered.
            # Wouldn't put it past this guy.
            print("WARNING: You might be stuck in a loop.")
            print(f'Current node: {current_node}')
            break

        for d in current_directions:
            
            if d == 'L':
                next_node = nodes[current_node][0]
            elif d == 'R':
                next_node = nodes[current_node][1]
            else:
                print(f'WARNING: Unrecognized direction {d}')

            steps += 1
            if next_node[-1] == 'Z':
                #print(f'Node found: {next_node}')
                # We're done
                lost = False
                current_node = next_node
                break
            else:
                current_node = next_node

            loop +=1

    new_path = path_dict.copy()
    new_path['current'] = current_node
    new_path['steps'] = path_dict['steps'] + steps

    return new_path


directions = ''
nodes = {}
with open(input_file, "r") as data:

    lines = data.readlines()

    i = 0
    for line in lines:
        # Grab the first line as the directions
        if i == 0:
            # Trim `\n`
            directions = line[:-1]
            i += 1

        else:
            # The node lines 
            if line.strip() != '': 
                data = line.split(' = ')
            
                node_name = data[0]
                branches = (data[1][1:-2].split(', '))

                node = (branches[0], branches[1])
                if node_name not in nodes.keys():
                    nodes[node_name] = node
                else:
                    print(f'WARNING: Duplicated node {node_name}')

#print(directions)
"""
for node, branch in nodes.items():
    print(f'{node}: {branch}')
"""

# For Part 2, let's see what we're dealing with
"""
for node, branch in nodes.items():
    if node[-1] == 'A':
        print(f'{node}: {branch}')
print('')
for node, branch in nodes.items():
    if node[-1] == 'Z':
        print(f'{node}: {branch}')
"""

"""
Strategy: Make a list of path dictionaries for each starting node '**A'
(there are 6).
Increment the first until it hits a '**Z'.  Then move the second up to that
number of steps.  If it's a '**Z', repeat with the others.  If it isn't,
then that's clearly not the answer, so go back to the first.
paths ~> [{'start':'JHA', 'current':'JFL', 'steps':1},
          {'start':'NCA', 'current':'FMN', 'steps':1}, ...]
"""

paths = []
for node in nodes.keys():
    if node[-1] == 'A':
        paths.append( {'start': node, 'current': node, 'steps': 0, 'hits':[]} )

"""
for path in paths:
    print(path)
"""
original_paths = paths

"""
print("Starting values:")
for path in paths:
    print(path)

new_paths = []
for path in paths:
    new_paths.append(increment_to_z(path, nodes, directions))
paths = new_paths

print('')
print("Increment 1:")
for path in paths:
    print(path)

new_paths = []
for path in paths:
    new_paths.append(increment_to_z(path, nodes, directions))
paths = new_paths

print('')
print("Increment 2:")
for path in paths:
    print(path)
"""

pd = {'start': 'TBZ', 'current': 'TBZ', 'steps': 21883, 'hits': []}
new_pd = increment_to_z(pd, nodes, directions)
print(new_pd)

"""
for i in range(1):

    # Based on this iteration, the minimum number of steps it could take
    min_steps = max([p['steps'] for p in paths])

    new_paths = []
    for path in paths:

        if path['steps'] < min_steps:
            new_paths.append(increment_to_z(path, nodes, directions))
        else:
            new_paths.append(path)
    
        paths = new_paths

    for path in paths:
        print(path)
"""

        
"""
    new_paths = []
    for path in paths:
        new_paths.append(increment_to_z(path, nodes, directions))
        paths = new_paths
"""
            
 
