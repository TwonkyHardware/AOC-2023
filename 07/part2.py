#!/usr/bin/python3

#input_file = "./sample_input_1"

input_file = "./input_1"


# Seems like I'm going to be doing lots of nonstandard sorting.
# Probably good to invest time in a class with a custom comparison function.
class Hand():
    """
    A class to represent a hand of cards, non-suited
    """

    #card_ordering = '23456789TJQKA'
    # New for Part 2:
    card_ordering = 'J23456789TQKA'

    # multiplicity tuple ~> (card count,
    #                        number of times that count appears in a hand)
    #
    # Ranking plus the multiplicity tuples used to identify them
    # in find_handtype
    hand_ordering = {'Five of a kind': [(5,1)],
                     'Four of a kind': [(4,1), (1,1)],
                     'Full house': [(3,1), (2,1)],
                     'Three of a kind': [(3,1), (1,2)],
                     'Two pair': [(2,2), (1,1)],
                     'One pair': [(2,1), (1,3)],
                     'High card': [(1,5)]
                     }

    def __init__(self, hand):
        # hand ~> 'KK677'

        self.hand = hand
        self.handtype = self.find_handtype(hand)


    def find_handtype(self, hand):
        # hand ~> 'KK677'

        # Easy adaptation for Part 2:
        # A little dab of recursion'll do ya
        if 'J' in hand:
            # Find handtypes for all values of J
            handtypes = []
            for card in self.card_ordering[1:]:
                # NB: There's never a time when you'll want multiple
                # J's to be different cards.
                try_hand = hand.replace('J', card)
                handtypes.append(self.find_handtype(try_hand))

            # Sort by listing in `hand_ordering{}`.  Lowest will be
            # the highest-ranking hand.
            handtypes.sort(key=lambda x: list(self.hand_ordering.keys()).index(x))
            return handtypes[0]

        # All J's will have been caught by the recursion loop.  We
        # now continue wild-card free, just as Part 1.
        rank_dict = {}
        for card in hand:
            if card not in rank_dict.keys():
                rank_dict[card] = 1
            else:
                rank_dict[card] += 1

        # rank_dict ~> {'K':2, '6':1, '7':2}
        #print(f'{hand}: {rank_dict}')

        count_list = list(rank_dict.values())
        count_set = set(count_list)
        multiplicity_list = []
        for count in count_set:
            multiplicity_list.append( (count, count_list.count(count)) )
        # multiplicity_list ~> [(1,1), (2,2)]
        #print(f'{hand}: {multiplicity_list}')

        for k,v in self.hand_ordering.items():
            if sorted(multiplicity_list) == sorted(v):
                #print(f'ml: {sorted(multiplicity_list)}')
                #print(f'v: {sorted(v)}')
                return k

        print(f"ERROR: hand type not found for hand {hand}")


    def __eq__(self, other):
        return (self.hand == other.hand)

    def __lt__(self, other):
        self_handtype = self.handtype
        other_handtype = other.handtype

        if self_handtype != other_handtype:
            # NB: Relying on Python dictionaries to maintain ordering.
            # Which they do now, but I always feel weird about it.
            self_rank = list(self.hand_ordering.keys()).index(self_handtype)
            other_rank = list(self.hand_ordering.keys()).index(other_handtype)
            return self_rank < other_rank

        else:
            for i,self_char in enumerate(self.hand):
                other_char = other.hand[i]
                if self_char == other_char:
                    continue
                else:
                    self_value = self.card_ordering.index(self_char)
                    other_value = self.card_ordering.index(other_char)
                    return self_value > other_value

        print("ERROR: card not orderable")


hands = []
with open(input_file, "r") as data:

    lines = data.readlines()
    for line in lines:

        data = line.split()
        hand = Hand(data[0])
        bid = data[1]

        hands.append( (hand, bid) )
        #print(f'{hand.hand}: {hand.handtype}')

# hands ~> [(<Hand 1>, '765'), (<Hand 2>, '684'), (<Hand 3>, '28'),
#           (<Hand 4>, '220'), (<Hand 5>, '483')]

hands.sort()
hands.reverse()
"""
for hand in hands:
    print(f'{hand[0].hand}: {hand[0].handtype}')
"""

total_winnings = 0
for i,hand in enumerate(hands):
    total_winnings += (i+1)*int(hand[1])

print(total_winnings)
# sample: 5909
# challenge: 252113488 -> correct!

