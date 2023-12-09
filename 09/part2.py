#!/usr/bin/python3

#input_file = "./sample_input_1"

input_file = "./input_1"

"""
Part 2: What sounds like a simple extension of Part 1
Update: Yeah, that took like 45 seconds
"""
with open(input_file, "r") as data:

    lines = data.readlines()

    tally = 0
    for line in lines:

        value_history = [int(n) for n in line.split()]
        # value_history ~> [10, 13, 16, 21, 30, 45]

        now_list = value_history
        derivatives = [now_list]
        check = True

        # Fill in the derivative lists
        while check:
            next_list = [ (now_list[i+1] - now_list[i])
                          for i in range(len(now_list)-1)]
            derivatives.append(next_list)

            # Check if there are only zeroes:
            deriv_set = set(next_list)
            if (len(deriv_set) == 1) and (0 in deriv_set):
                check = False

            now_list = next_list

        """
        for d in derivatives:
            print(d)
        """

        # Work backwards through the derivative list
        derivs = list(reversed(derivatives))
        new_derivatives = []
        increment = 0
        for deriv in derivs:
            new_value = deriv[0] - increment
            deriv.insert(0, new_value)
            new_derivatives.insert(0, deriv)
            increment = deriv[0]

        """
        for nd in new_derivatives:
            print(nd)
        print('')
        """

        # Tally all of the new values as we go
        tally += new_derivatives[0][0]

print(tally)
# tally = 884
# Correct!







