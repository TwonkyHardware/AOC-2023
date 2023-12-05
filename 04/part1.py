#!/usr/bin/python3

#input_file = "./sample_input_1"

input_file = "./input_1"

scores = {}
with open(input_file, "r") as data:
    lines = data.readlines()
    for line in lines:

        data_split = line.split(':')

        card_key = data_split[0].strip()
        # card_key ~> 'Card 1'

        card_data = data_split[1].strip()
        # card_data ~> `41 48 83 86 17 | 83 86  6 31 17  9 48 53`

        data_sets = card_data.split('|')

        win_nums = data_sets[0].strip()
        win_nums = set(win_nums.split())
        # win_nums ~> {'83', '48', '17', '41', '86'}

        play_nums = data_sets[1].strip()
        play_nums = set(play_nums.split())
        # play_nums ~> {'83', '9', '6', '48', '17', '86', '53', '31'}

        union = win_nums & play_nums
        #print(union)

        if len(union) == 0:
            scores[card_key] = 0
        else:
            scores[card_key] = 2**(len(union)-1)

for k,v in scores.items(): print(f'{k}: {v}')
# scores ~> {'Card 1': 8, 'Card 2': 2, 'Card 3': 2, 'Card 4': 1, 'Card 5': 0, 'Card 6': 0}

result = sum(scores.values())
print(result)
            
