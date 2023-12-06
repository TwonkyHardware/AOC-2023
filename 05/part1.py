#!/usr/bin/python3

#input_file = "./sample_input_1"

# Proper attempt at Part 1.
input_file = "./input_1"


def map_number(source_type, source_value, maps, seed=None):
    """
    Given an input map type and value, use `maps{}` to find the 
    output type and value

    source_type ~> 'seed', 'water', ...
    source_value ~> 45, 56, ...
    maps ~>
    {('seed','soil'): [{'offset_range': (source_start, source_start + range_length),
                        'offset_base': dest_start},
                       {'offset_range': (source_start, source_start + range_length),
                        'offset_base': dest_start},
                       ... ], ... }
    """

    #print(f'{source_type}, {source_value}')
    for map_key,range_list in maps.items():
        if source_type == map_key[0]:
            # We've found the right map
            target_type = map_key[1]
            target_value = None
            
            for range_dict in range_list:
                low = range_dict['offset_range'][0]
                high = range_dict['offset_range'][1]
                base = range_dict['offset_base']

                if source_value in range(low, high):
                    # We've found the right range.
                    # Find the offset: the difference between the source
                    # value and the base of its range
                    offset = source_value - low
                    target_value = base + offset

            # If we've been through all range_dicts without finding
            # a range and target value, the mapping is direct
            if not target_value:
                target_value = source_value
                # Good debugging test case
                #print(f'seed: {seed}, source type: {source_type}, source value: {source_value}')

            # return ~> ('water', 77)
            return (target_type, target_value)

    print("ERROR: source map type not found")
    return


# `maps{}` will be the primary data object for the challenge
maps = {}
"""
maps ~>
 {('seed','soil'): [{'offset_range': (source_start, source_start + range_length),
                     'offset_base': dest_start},
                    {'offset_range': (source_start, source_start + range_length),
                     'offset_base': dest_start},
                    ... ],
  ('soil','fert'): [{'offset_range': (source_start, source_start + range_length),
                     'offset_base': dest_start},
                    {'offset_range': (source_start, source_start + range_length),
                     'offset_base': dest_start},
                    ... ],
  ... }
"""

# Store the input seed numbers
seeds = []

# Use these to track map data in the read-in loop
current_map_key = None
current_ranges_list = []

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
            current_ranges_list = []

        elif line == '':
            # We're done with the current map.  Add it to `maps{}`
            if current_ranges_list:
                maps[current_map_key] = current_ranges_list
            # The next endswith('map:') will reset `current_map{}`
            # and `current_map_key`.

        elif line[0].isdigit():
            numbers = list( int(n) for n in line.split() )
            # numbers ~> [50, 98, 2]

            dest_start = int(numbers[0])
            source_start = int(numbers[1])
            range_length = int(numbers[2])

            # NB: Upper limit of 'offset range' is 1 more than the real upper
            # limit.  Since we'll be using `range()` to analyze it, it'll work
            # out.
            current_range_dict = {
                'offset_range': (source_start, source_start + range_length),
                'offset_base': dest_start
            }
            current_ranges_list.append(current_range_dict)

# Input ends before final map is complete
if current_ranges_list:
    maps[current_map_key] = current_ranges_list
#for k,v in maps.items(): print(f'{k}: {v}')

#print(seeds)

# Now navigate the maps.
locations = []
for seed in seeds:

    # Starting source:
    source_type = 'seed'
    source_value = int(seed)

    target_type = ''
    target_value = ''

    while target_type != 'location':
        map_result = map_number(source_type, source_value, maps, seed=seed)
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
