#!/usr/bin/python3

input_file = "./input"
#input_file = "./test_input_2"

digit_strings = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}

total = 0
with open(input_file, "r") as data:
    lines = data.readlines()
    for line in lines:

        first = None
        while not first:
            if line[0].isdigit():
                first = line[0]
            else:
                for k,v in digit_strings.items():
                    if line[0:len(k)] == k:
                        first = str(v)

            if not first:
                line = line[1:]


        last = None
        while not last:
            if not line:
                last = first
                break

            if line[-1].isdigit():
                last = line[-1]
            else:
                for k,v in digit_strings.items():
                    if line[-len(k):] == k:
                        last = str(v)

            if not last:
                line = line[:-1]
                
        num = first + last
        total += int(num)
        # Spot check:
        #print(f'{line.strip()}: {num}')


print(f'Total: {total}')
