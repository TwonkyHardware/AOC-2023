#!/usr/bin/python3

#input_file = "./sample_input_1"

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


def fill_gap_blocks(block_list):
    """
    block_list ~> 
    [{'in_block': (0, 597716), 'out_block': (1288156819, 1288754535)},
     {'in_block': (597717, 5296455), 'out_block': (1225532780, 1230231518)},
     {'in_block': (5296456, 529385086), 'out_block': (2165784541, 2689873171)},
     ...]
    """
    # Can assume list is sorted by first value of 'in_block'

    filled_list = []
    last_high = -1
    for block_dict in block_list:
        # block_dict ~> {'in_block': (0, 597716),
        #                'out_block': (1288156819, 1288754535)}

        block_low = block_dict['in_block'][0]
        # block_low ~> 0
        block_high = block_dict['in_block'][1]
        # block_high ~> 597716

        # Check low bound against the previous high
        if block_low == last_high + 1:
            # This fits in after the previous block, so add it and move on
            filled_list.append(block_dict)
        elif block_low < (last_high + 1):
            print(f"ERROR: block mismatch at {block_low}")
        else:
            # We need a new block to fill in.  These numbers map directly.
            new_block = {'in_block': ( (last_high + 1), (block_low - 1) ),
                         'out_block': ( (last_high + 1), (block_low - 1) )}
            filled_list.append(new_block)

        last_high = block_high

    return_list = sorted(filled_list, key=lambda dic: dic['in_block'][0])

    return return_list


def check_out_gaps(key, block_list):
    """
    fill_gap_blocks() ensures there are no gaps in in_block listings.
    This check to see if there are any in the out_block listings.
    Hopefully there are not.
    """
    """
    block_list ~> 
    [{'in_block': (0, 597716), 'out_block': (1288156819, 1288754535)},
     {'in_block': (597717, 5296455), 'out_block': (1225532780, 1230231518)},
     {'in_block': (5296456, 529385086), 'out_block': (2165784541, 2689873171)},
     ...]
    """

    # Re-sort by 'out-block'
    out_list = sorted(block_list, key=lambda dic: dic['out_block'][0])
    #print(f'{key}:')
    #print(out_list)

    last_high = -1
    for block_dict in out_list:
        # block_dict ~> {'in_block': (0, 597716),
        #                'out_block': (1288156819, 1288754535)}

        block_low = block_dict['out_block'][0]
        # block_low ~> 1288156819
        block_high = block_dict['out_block'][1]
        # block_high ~> 1288754535

        # Check low bound against the previous high
        if block_low == last_high + 1:
            # This fits in after the previous block, so move on
            last_high = block_high
            continue

        elif block_low < (last_high + 1):
            print(f"ERROR: block mismatch at {block_low}")
        else:
            print(f"WARNING: Output gap block found in {key}: {last_high + 1} -> {block_low - 1}")

        last_high = block_high

    return
    

def find_originating_blocks(key, maps, input_block_list):
    """
    A 'block' is a set of values in a mapping that maps to or from
    the other side of the mapping with the same offset.

    For a list of blocks in the 'output' values of the mapping indicated
    by `key`, find this list of blocks in the 'input' values that can
    map to them.
    """
    # key ~> ('seed', 'soil')
    # input_block_list ~>
    # [(274008432, 489813286), (656837795, 1129193792), (0, 145118816),
    #  (1129193793, 1167459709), (209454928, 274008431)]

    map_list = maps[key].copy()
    map_list = sorted(map_list, key=lambda dic: dic['out_block'][0])
    block_list_in = input_block_list.copy()
    block_list_out = []

    for block_in in block_list_in: 

        overlap_found = False

        for block_dict in map_list:
            """
            block_dict ~> {'in_block': (240637693, 336470526),
                           'out_block': (35419402, 131252235)}
            """

            in_range = block_dict['in_block']
            out_range = block_dict['out_block']
            low = out_range[0]
            high = out_range[1]

            threshold_low = block_in[0]
            threshold_high = block_in[1]

            if low > threshold_high:
                #print("low > threshold_high recognized")
                overlap_found = False
                continue
            elif low <= threshold_low and high > threshold_low:
                #print(f'low {low} <= threshold low {threshold_low} recognized')
                #print(f'high {high} > threshold low {threshold_low} recognized')

                overlap_found = True
                if in_range not in block_list_out:
                    block_list_out.append(in_range)

            elif overlap_found and low > threshold_low:
                #print(f'low {low} > threshold low {threshold_low} recognized')
                if in_range not in block_list_out:
                    block_list_out.append(in_range)

    return block_list_out


"""
`maps{}` will be the primary data object for the challenge.
The mappings from the source to the destination categories define what I 
will call "blocks."
A 'block' is a set of values in a mapping that maps to or from
the other side of the mapping with the same offset.
"""
maps = {}
"""
maps ~>
 {('seed','soil'): [{'in_block': (source_start, source_start + range_length),
                     'out_block': (dest_start, dest_start + range_length)},
                    {'in_block': (source_start, source_start + range_length),
                     'out_block': (dest_start, dest_start + range_length)},
                    ... ],
  ('soil','fert'): [{'in_block': (source_start, source_start + range_length),
                     'out_block': (dest_start, dest_start + range_length)},
                    {'in_block': (source_start, source_start + range_length),
                     'out_block': (dest_start, dest_start + range_length)},
                    ... ],
  ... }
"""

# Store the input seed numbers
seeds = []

# Use these to track map data in the read-in loop
current_map_key = None
current_ranges_list = []

seed_ranges = []
with open(input_file, "r") as data:
    lines = data.readlines()
    for line in lines:

        line = line.strip()

        if line.startswith('seeds:'):
            seeds += list(line[7:].split())

            seeds = [int(seed) for seed in seeds]
            # For part 2, `seeds` now defines ranges.
            # Ranges cover > 2 billion, so individual calculations are impossible

            for i in range(0, len(seeds), 2):
                # NB: Upper range is one too much.  Make sure future use
                # of range() corrects this, or do it here.
                seed_ranges.append( (seeds[i], seeds[i] + seeds[i+1]) )

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

            # `-1` because block includes the lower bound
            current_range_dict = {
                'in_block': (source_start, source_start + range_length - 1),
                'out_block': (dest_start, dest_start + range_length - 1)
            }
            current_ranges_list.append(current_range_dict)

# Input ends before final map is complete
if current_ranges_list:
    maps[current_map_key] = current_ranges_list
#for k,v in maps.items(): print(f'{k}: {v}')

# Sort the lists
new_maps = {}
for k,v in maps.items():
    new_v = sorted(v, key=lambda dic: dic['in_block'][0])
    new_maps[k] = new_v
maps = new_maps
#for k,v in maps.items(): print(f'{k}: {v}')

# Fill in gaps
new_maps = {}
for k,v in maps.items():
    new_v = fill_gap_blocks(v)
    new_maps[k] = new_v
maps = new_maps
"""
for k,v in maps.items():
    print(f'{k}:')
    for lst in v:
        print(f'{lst}')
"""
# There are gaps in some of the output ends of the maps.
# I assume we have to assume these are unreachable?
#for k,v in maps.items():
#    check_out_gaps(k,v)

#print(seeds)

"""
Now work backwards through the maps in the hope that the lowest location block
maps to a seed block of reasonable size to search.
This gets messy.  I never cleaned it up because (spoiler) it was not successful.
"""
new_list = maps[('humidity', 'location')].copy()
new_list = sorted(new_list, key=lambda dic: dic['out_block'][0])
location_low_range = new_list[0]['out_block']
#print(location_low_range)

humidity_low_range = new_list[0]['in_block']
#print(humidity_low_range)
# ~> (387558480, 528873168)


# Find humidity blocks of the ('temperature', 'humidity') map
# that feed into the humidity low range.
# This immediately works backwards to the temperature blocks.
next_block_list = find_originating_blocks(('temperature', 'humidity'), maps, [humidity_low_range])
#print(temperature_block_list)
# ~> [(336470527, 827398048)]
# Maps to humidity range (348097907, 839025428)
# mapping entirely contains the humidity low range (387558480, 528873168)


# Find temperature blocks of the ('light', 'temperature') map
# that feed into the temperature low range.
# This immediately works backwards to the light blocks.
next_block_list = find_originating_blocks(('light', 'temperature'), maps, next_block_list)
#print(next_block_list)
"""
[(570877057, 812004213), (812004214, 1007855621), (358179343, 379172139), (327707746, 358179342), (421331130, 570877056)]

These light blocks map to temperature blocks

(570877057, 812004213)  -> (300892136, 542019292)
(812004214, 1007855621) -> (542019293, 737870700)
(358179343, 379172139)  -> (737870701, 758863497)
(327707746, 358179342)  -> (758863498, 789335094)
(421331130, 570877056)  -> (789335095, 938881021)

Together, these entirely cover the temperature minimum range 
(336470527, 827398048)
"""


# Find temperature blocks of the ('water', 'light') map
# that feed into the light low ranges.
# This immediately works backwards to the water blocks.
next_block_list = find_originating_blocks(('water', 'light'), maps, next_block_list)
#print(next_block_list)
"""
[(274008432, 489813286), (656837795, 1129193792), (0, 145118816), (1129193793, 1167459709), (209454928, 274008431)]

These water blocks map to light blocks

(274008432, 489813286)   -> (498004792, 713809646)
(656837795, 1129193792)  -> (713809647, 1186165644)
(0, 145118816)           -> (250066554, 395185370)
(1129193793, 1167459709) -> (395185371, 433451287)
(209454928, 274008431)   -> (433451288, 498004791)

Or, putting the light blocks in order,
(250066554, 395185370)
(395185371, 433451287)
(433451288, 498004791)
(498004792, 713809646)
(713809647, 1186165644)

Together, these light blocks entirely cover the light minimum ranges 
(327707746, 358179342)
(358179343, 379172139)
|                    |
(421331130, 570877056)
(570877057, 812004213)
(812004214, 1007855621)

Note that there's a gap in the overall light minimum ranges
from (379172140, 421331129)
"""


# Find temperature blocks of the ('fertilizer', 'water') map
# that feed into the water low ranges.
# This immediately works backwards to the fertilizer blocks.
next_block_list = find_originating_blocks(('fertilizer', 'water'), maps, next_block_list)
#print(next_block_list)
"""
[(690472942, 822897255), (119745763, 160132681), (486420845, 553340957), (553340958, 583517502), (1840321280, 2112070263), (2248438960, 2390857911), (583517503, 690472941), (236670371, 461310334)]

These fertilizer blocks map to water blocks

(690472942, 822897255)   -> (224639964, 357064277)
(119745763, 160132681)   -> (357064278, 397451196)
(486420845, 553340957)   -> (397451197, 464371309)
(553340958, 583517502)   -> (464371310, 494547854)
(1840321280, 2112070263) -> (650698701, 922447684)
(2248438960, 2390857911) -> (922447685, 1064866636)
(583517503, 690472941)   -> (1064866637, 1171822075)
(236670371, 461310334)   -> (0, 224639963)

Or, putting the water blocks in order,
(0,         224639963)
(224639964, 357064277)
(357064278, 397451196)
(397451197, 464371309)
(464371310, 494547854)
|                    |
(650698701, 922447684)
(922447685, 1064866636)
(1064866637, 1171822075)

Together, these entirely cover the water minimum ranges 
(0, 145118816)
(209454928, 274008431)
(274008432, 489813286)
(656837795, 1129193792)
(1129193793, 1167459709)
"""

# Find fertilizer blocks of the ('soil', 'fertilizer') map
# that feed into the fertilizer low ranges.
# This immediately works backwards to the soil blocks.
next_block_list = find_originating_blocks(('soil', 'fertilizer'), maps, next_block_list)
#print(next_block_list)
"""
[(510011966, 917612383), (1190058688, 1443940248), (278649209, 510011965), (1080212773, 1190058687), (917612384, 1080212772), (2020920273, 2073349244), (3676064680, 3963972224), (4033128077, 4213457984), (1664441438, 1817839801), (2000795920, 2020920272)]
"""

# Find seed blocks of the ('seed', 'soil') map
# that feed into the soil low ranges.
# This immediately works backwards to the seed blocks.
next_block_list = find_originating_blocks(('seed', 'soil'), maps, next_block_list)
print(next_block_list)
"""
[(2324624490, 2651206327), (529385087, 1034793204), (2977305241, 3018234601), (597717, 5296455), (1034793205, 1092718504), (0, 597716), (1682469958, 1738931329), (2259042282, 2285166784), (3442489267, 3852307367), (1894195346, 2209682248), (1857068786, 1894195345), (1603988885, 1682469957), (2671974456, 2750010915), (1092718505, 1603988884), (2285166785, 2324624489)]

These are the seed numbers that can feed into the lowest block of locations.

In order:
(            0,       597 716)
(      597 717,     5 296 455)
(  529 385 087, 1 034 793 204)
(1 034 793 205, 1 092 718 504)
(1 092 718 505, 1 603 988 884)
(1 603 988 885, 1 682 469 957)
(1 682 469 958, 1 738 931 329)
|                      |
(1857068786, 1894195345)
(1894195346, 2209682248)
|                      |
(2259042282, 2285166784)
(2285166785, 2324624489)
(2324624490, 2651206327)
|                      |
(2671974456, 2750010915)
|                      |
(2977305241, 3018234601)
|                      |
(3442489267, 3852307367)

That's still too many to check.

Potential seed ranges for my data are
( 20 816 377, 596 708 258)
(763 445 965, 785 702 22)
(1693788857, 146680070)
(1157620425, 535920936)
(3187993807, 180072493)
(1047354752, 20193861)
(2130924847, 274042257)
(950268560, 11451287)
(3503767450, 182465951)
(3760349291, 265669041)

The overlap leaves billions of seeds to check still.

I give up.
Could've done a better job keeping the ranges narrow by splitting overlapping blocks and discarding the parts that didn't overlap.
I don't think that would have been a magic bullet, though.
Probably also need to start at the lowest location and work backwards one-by-one to see if each ends up in one of the target seed ranges.

Wild guess: 179684458

That's wrong.  Too high.
"""


# Now navigate the maps.
# Commented out while I tried to narrow down the selection range above.
# Did not work.
locations = []
"""
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

    '''
    Seed 79 -> Location 82
    Seed 14 -> Location 43
    Seed 55 -> Location 86
    Seed 13 -> Location 35
    '''
"""

#result = min(locations)
#print(f'Lowest location value: {result}')





