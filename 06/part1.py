#!/usr/bin/python3
# 1st import of AoC 2023
import math

#input_file = "./sample_input_1"

input_file = "./input_1"

with open(input_file, "r") as data:

    times = []
    distances = []

    lines = data.readlines()
    for line in lines:

        if line.startswith('Time:'):
            line = line.replace('Time:','')
            line.strip()
            times = [int(n) for n in line.split()]

        if line.startswith('Distance:'):
            line = line.replace('Distance:','')
            line.strip()
            distances = [int(n) for n in line.split()]

#print(times)
#print(distances)
records = [(times[i], distances[i]) for i in range(len(times))]
#print(records)
# records ~> [(7, 9), (15, 40), (30, 200)]


# Call the button press time t1 and the travel time t2.
# The total race time is T; T = t1 + t2.
# The press time that results in the greatest distance is t0.
# t0 = T/2.
# Record race distance is D.

# Strategy 1: is to start at t0 and work outward to find out how many cases win.
# This enumerates all win cases.  Fortunately, unlike yesterday, there are an
# enumerable number of cases in the challenge data.
# Unused for Part 1.
for record in records:
    T = record[0]
    D = record[1]
    wins = []

    # This is the optimum time.  If the race can be won, it will
    # be won for this t1
    t0 = int(T/2)

    t1 = t0
    # `d` is the distance the boat travels under a given t1.
    # Start at the maximum.
    d = t1*(T-t1)

    # First check downward
    while d > D:
        wins.append(t1)
        t1 -= 1
        d = t1*(T-t1)

    # Then check upward
    t1 = t0 + 1
    d = t1*(T-t1)
    while d > D:
        wins.append(t1)
        t1 += 1
        d = t1*(T-t1)

    wins.sort()
    #print(wins)


# Strategy 2: Use algebra to solve for the t1's that represent distances d
# in excess of D, then count the number of integers between them.  This saves
# us from having to enumerate cases in case the numbers get large.
num_wins = []
for record in records:
    T = record[0]
    D = record[1]
    
    # Solve the quadratic equation for times that will beat D
    # t1 = [ T +/- sqrt(T^2 - 4D) ]/2
    rad = T**2 -4*D
    #print(rad)
    
    # If rad < 0, there are no real intersections t1 and D, and thus no
    # possibility of winning
    if rad >=0:
        t_low = T/2 - math.sqrt(rad)/2
        t_high = T/2 + math.sqrt(rad)/2
    else:
        print(f'WARNING: No solution for Race Time {T} and Record Distance {D}')

    #print(f'{t_low}, {t_high}')

    # `t_low` and `t_high` are floats.  Convert them to the appropriate
    # integer.
    # NB: If they're already integers in float form, they aren't valid
    # solutions because they indicate a t1 that will *tie* D.  We need
    # them to *exceed* D, so bump them to the next int.
    if t_low.is_integer():
        t_low = int(t_low + 1)
    else:
        t_low = math.ceil(t_low)

    if t_high.is_integer():
        t_high = int(t_high - 1)
    else:
        t_high = math.floor(t_high)
    #print(f'{t_low}, {t_high}')

    num_wins.append(len(range(t_low, t_high)) + 1)

print(num_wins)

result = 1
for n in num_wins:
    result *= n

print(result)
# result ~> 4403592
