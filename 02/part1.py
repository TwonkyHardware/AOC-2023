#!/usr/bin/python3

#input_file = "./sample_input_1"
input_file = "./input_1"

colors = ['red', 'green', 'blue']

game_data = {}

with open(input_file, "r") as data:
    lines = data.readlines()
    for line in lines:

        data_split = line.split(':')

        game_key = data_split[0].strip()
        # game_key ~> 'Game 1'

        results_list = data_split[1].strip()
        #results_list ~> '3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green'

        try_sets = results_list.split(';')
        try_sets = [ts.strip() for ts in try_sets]
        # try_sets ~> ['3 blue, 4 red', '1 red, 2 green, 6 blue', '2 green']

        try_dicts = []
        for cube_set in try_sets:
            # cube_set ~> '1 red, 2 green, 6 blue'

            color_sets = cube_set.split(',')
            color_sets = [cs.strip() for cs in color_sets]
            # color_sets ~> ['1 red', '2 green', '6 blue']

            try_dict = {c:0 for c in colors}
            for color_set in color_sets:
                color_datum = color_set.split()
                try_count = color_datum[0]
                try_color = color_datum[1]

                try_dict[try_color] += int(try_count)

            try_dicts.append(try_dict)

        # try_dicts ~> [{'blue':3, 'red':4},
        #               {'red':1, 'green':2, 'blue':6},
        #               {'green':2}]

        game_data[game_key] = try_dicts
        # game_data ~> {'Game 1': [{'blue':3, 'red':4},
        #                          {'red':1, 'green':2, 'blue':6},
        #                          {'green':2}],
        #               'Game 2': ... }


game_minima = {}
for game,data in game_data.items():
    minima = {c:0 for c in colors}
    minima['total'] = 0

    for try_dict in data:
        # try_dict ~> {'red':1, 'green':2, 'blue':6}
        for color, count in try_dict.items():
            if minima[color] < count:
                minima[color] = count

        # total figured by number seen at once
        total = sum([num for num in try_dict.values()])
        if minima['total'] < total:
            minima['total'] = total

    # minima ~> {'red': 4, 'green': 2, 'blue': 6, 'total': 9}

    # total figured by sum of individual minima
    total_by_color = sum([minima[c] for c in colors])
    if total_by_color > minima['total']:
        minima['total'] = total_by_color

    game_minima[game] = minima

# game_minima ~> {'Game 1': {'red': 4, 'green': 2, 'blue': 6, 'total': 12},
#                 'Game 2': {'red': 1, 'green': 3, 'blue': 4, 'total': 8},
#                 ...}

limits = {'red':12, 'green':13, 'blue':14}

possible_games = []
for game,data in game_minima.items():
    possible = True
    for c in colors:
        if data[c] > limits[c]:
            possible = False
            break

    if possible:
        possible_games.append(game)

game_numbers = [int( game.replace('Game ','') ) for game in possible_games]

result = sum(game_numbers)
print(game_numbers)
print(result)
