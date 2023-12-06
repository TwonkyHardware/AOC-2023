#!/usr/bin/python3

#input_file = "./sample_input_1"

"""
My initial attempt at Part 1.
Didn't look at the input data until after getting this to work with the
sample input.
The method here of filling in the entire mapping dictionary is far too
inefficient for such large numbers as in the test input.  Had to force quit
before my laptop melted.  Lesson learned!
"""
#input_file = "./input_1"


def map_number(source_type, source_value, maps):
    """
    Given an input map type and value, use `maps{}` to find the 
    output type and value

    source_type ~> 'seed', 'water', ...
    source_value ~> 45, 56, ...
    maps ~> {('seed','soil'):{0:0, 1:1, ..., 50:52, ..., 99:51}, ... }
    """

    #print(f'{source_type}, {source_value}')
    for k,v in maps.items():
        if source_type == k[0]:
            target_type = k[1]
            #print(v)
            target_value = v[source_value]

            # return ~> 'water', 77
            return (target_type, target_value)

    print("ERROR: source map type not found")
    return


seeds = []
maps = {}
# maps ~> {('seed','soil'):{0:0, 1:1, ..., 50:52, ..., 99:51}, ... }

# A priori, we don't know how high numbers might go.  Track with `max_number`
max_number = 0

# Use these to track map data in the read-in loop
current_map_key = None
current_map = {}

with open(input_file, "r") as data:
    lines = data.readlines()
    for line in lines:

        line = line.strip()

        if line.startswith('seeds:'):
            seeds += list(line[7:].split())

        elif line.endswith('map:'):
            map_label = line[:-5]
            map_parts = map_label.split('-to-')
            map_type = (map_parts[0], map_parts[1])
            # map_type ~> ('seed', 'soil')

            current_map_key = map_type
            current_map = {}

        elif line == '':
            # We're done with the current map.  Add it to `maps{}`
            if current_map:
                maps[current_map_key] = current_map
            # The next endswith('map:') will reset `current_map{}`
            # and `current_map_key`.

        elif line[0].isdigit():
            numbers = list( int(n) for n in line.split() )
            # numbers ~> [50, 98, 2]
            #print(numbers)

            # Add to the current map
            for i in range(numbers[2]):
                current_map[numbers[1]+i] = numbers[0]+i

                # Track the maximum number
                if numbers[0]+i > max_number:
                    max_number = numbers[0]+i
                if numbers[1]+i > max_number:
                    nax_number = numbers[1]+i

# Input ends before final map is complete
if current_map:
    maps[current_map_key] = current_map
#for k,v in maps.items(): print(f'{k}: {v}')

#print(seeds)
#print(max_number)
# max_number ~> 99

# With `maps{}` complete for explicit input data, fill in the implicit data
# up to max_number
new_maps = {}
for k,v in maps.items():
    for i in range(max_number + 1):
        if i not in v.keys():
            v[i] = i
    # Sort for readability
    new_v = dict(sorted(v.items()))
    new_maps[k] = new_v

maps = new_maps

#for k,v in maps.items(): print(f'{k}: {v}')
#for v in maps.values(): print(len(v))

# Now navigate the maps.
locations = []
for seed in seeds:

    # Starting source:
    source_type = 'seed'
    source_value = int(seed)

    target_type = ''
    target_value = ''

    while target_type != 'location':
        map_result = map_number(source_type, source_value, maps)
        # Double-up on variable names for readability
        target_type = map_result[0]
        target_value = map_result[1]
        source_type, source_value = target_type, target_value
        
    locations.append(target_value)
    print(f'Seed {seed} -> Location {target_value}')
    """
    Seed 79 -> Location 82
    Seed 14 -> Location 43
    Seed 55 -> Location 86
    Seed 13 -> Location 35
    """

result = min(locations)
print(f'Lowest location value: {result}')
