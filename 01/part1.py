#!/usr/bin/python3

input_file = "./input"

total = 0
with open(input_file, "r") as data:
    lines = data.readlines()
    for line in lines:

        nums = []
        for char in line:
            if char.isdigit():
                nums.append(char)

        num = nums[0] + nums[-1]
        total += int(num)
        # Spot check:
        #print(f'{line.strip()}: {num}')

print(f'Total: {total}')
