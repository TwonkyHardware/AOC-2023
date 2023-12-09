#!/usr/bin/python3

#input_file = "./sample_input_1"
#input_file = "./sample_input_2"

input_file = "./input_1"

directions = ''
repeat_directions = directions
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
# Goddamn it
# IF you're going from the first node on the list to the last, this is correct:
#starting_node = list(nodes.keys())[0]
#target_node = list(nodes.keys())[-1]
# However, that's evidently not what the challenge is.  This is:
starting_node = 'AAA'
target_node = 'ZZZ'

print(f'Starting node: {starting_node}')
print(f'Target node: {target_node}')

current_node = starting_node
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

    for d in directions:

        if d == 'L':
            next_node = nodes[current_node][0]
        elif d == 'R':
            next_node = nodes[current_node][1]
        else:
            print(f'WARNING: Unrecognized direction {d}')

        #print(f'd = {d}')
        #print(f'next_node_name = {next_node_name}')
        print(f'{d}  {current_node} {nodes[current_node]} -> {next_node}')

        steps += 1
        if next_node == target_node:
            #print(f'{next_node}')
            #print(f'{target_node.name}')
            # We're done
            lost = False
            break
        else:
            current_node = next_node

    loop +=1

if loop != limit:
    print(steps)
# steps = 264
# Too low?
# Check manually
# Manual check results in the same.
"""
So.  The termination conditions are not well articulated by the author.  In both examples, we go from AAA to ZZZ, which happen to be the first and last entries on the list.  I don't think it's unreasonable to read that as "go from the first entry to the last entry" with AAA and ZZZ as obvious placeholders.
Evidently that's wrong, though.  I'm to go from AAA to ZZZ literally.
"""
# Going from AAA to ZZZ, the answer is
# steps = 16343
