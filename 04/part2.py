#!/usr/bin/python3

#input_file = "./sample_input_1"

input_file = "./input_1"

# Pull and store the data as a list of dictionaries
# cards ~> [{'key':'Card   1', 'number':1, 'count':1, 'wins': 2}, ... ]
cards = []
with open(input_file, "r") as data:
    lines = data.readlines()
    for line in lines:

        card = {}

        data_split = line.split(':')

        key = data_split[0].strip()
        card['key'] = key.strip()
        # card['key'] ~> 'Card 1'

        card['number'] = int(key[4:].strip())
        # card['number'] ~> 1

        card['count'] = 1

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

        card['wins'] = len(union)

        cards.append(card)

#for card in cards: print(card)
# Sort for safety
cards.sort(key=lambda card: card['number'])
#print(cards)

# Now loop through cards.
# Store results in a dictionary
accounted_cards = {}
# accounted_cards ~> {'Card 1': 1, 'Card 2': 2, 'Card 3': 4, ... }

# Track extra cards in a rotation dictionary.
extra_cards = {}
# extra_cards ~> { <card number>: <extra count> }
#             ~> {1:2, 2:1, 3:0, 4:1, ...}

# Don't want to loop over cards[] while I perform operations on it, so
# instead loop over the number of things I know it has in it.
num_cards = len(cards)
for i in range(num_cards):

    # Pop so the next card is always at the front of the queue.
    card = cards.pop(0)
    #print(f'card: {card}')

    number = i+1
    card_index = i+1
    if card_index != card['number']:
        print(f"Warning: card index mismatch for {card['key']}")

    # See if there are extra cards for this card.
    # Add to total if so.
    total_cards = card['count']
    #print(f'Starting extra cards: {extra_cards}')
    if card_index in extra_cards.keys():
        total_cards += extra_cards[card_index]
        # Don't need to track this anymore
        del extra_cards[card_index]
        #print(f'Deleting record of card # {card_index}. Extra cards: {extra_cards}')

    #print(f"Total cards for {card['key']}: {total_cards}")
    # Record how many of these cards I have in total
    accounted_cards[card['key']] = total_cards

    # Now keep track of how many extra cards I get for future cards
    wins = card['wins']

    """
    if wins:
        print_range = ','.join(
            [str(num+1) for num in list(range(card_index, card_index + wins))]
        )
        print(f'Adding {total_cards} cards for card numbers {print_range}')
    """
    for j in range(card_index, card_index + wins):
        index = j+1
        # `index` will be the card numbers of the cards I get more of
        if index in extra_cards.keys():
            extra_cards[index] += total_cards
        else:
            extra_cards[index] = total_cards
    #print(f'Final extra cards: {extra_cards}\n')

#print(accounted_cards)
# accounted_cards ~> {'Card 1': 1, 'Card 2': 2, 'Card 3': 4, 'Card 4': 8,
#                     'Card 5': 14, 'Card 6': 1}

result = sum( [n for n in accounted_cards.values()] )
print(result)
# result = 9236992
