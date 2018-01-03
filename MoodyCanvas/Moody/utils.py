import math

#   Subtract first value from all the rest of the measurements.
#   This eliminates a need to have the first measurement be zero.
def sub_first(line):
    return_line = []
    sub = line[0]
    for meas in line:
        return_line.append(meas - sub)
    return return_line

#   Add each measurement to the sum of those before it.
def add_rows(line):
    return_line = []
    last = 0;
    for meas in line:
        last += meas
        return_line.append(last)
    return_line.insert(0,0)
    return return_line

#   Performing this function on the diagonal lines
#   sets the center of the plate to zero
def process_diag(line, foot):
    corr = line[-1] / (len(line) - 1)
    middle = round((len(line) - 1) / 2)
    return_line = list(range(len(line)))
    return_line[middle] = -line[middle]
    count = 1
    while count <= middle:
        return_line[middle-count] = return_line[middle-(count-1)] + corr
        count += 1
    count = 1
    while count <= middle:
        return_line[middle+count] = return_line[middle+(count-1)] - corr
        count += 1
    count = 0
    for meas in return_line:
        return_line[count] += line[count]
        count += 1
    return return_line

#   Make ends of perimeter lines match with ends of diagonals
def process_line(line, foot, corner1, corner2):
    return_line = list(range(len(line)))
    return_line[-1] = corner2 - line[-1]
    corr = (return_line[-1] - corner1) / (len(line) - 1)
    count = -2
    while -count <= len(line):
        return_line[count] = return_line[count+1] - corr
        count -= 1
    count = 0
    while count < len(line):
        return_line[count] += line[count]
        count += 1
    return return_line

def get_mid(line1, line2):
    return [line1[round(len(line1) / 2 - .5)], line2[round(len(line2) / 2 - .5)] ]

def get_height_map(profiles, foot):
    foot = int(foot)
    count = 0
    holder_profile = []
    holder_profiles = []
    for profile in profiles:
        holder_profile = sub_first(profile)
        holder_profile = add_rows(holder_profile)
        profiles[count] = holder_profile
        count += 1
    profiles[0] = process_diag(profiles[0], foot)
    profiles[1] = process_diag(profiles[1], foot)
    profiles[2] = process_line(profiles[2], foot, profiles[1][0], profiles[0][0])
    profiles[3] = process_line(profiles[3], foot, profiles[0][0], profiles[1][0])
    profiles[4] = process_line(profiles[4], foot, profiles[1][0], profiles[0][0])
    profiles[5] = process_line(profiles[5], foot, profiles[0][0], profiles[1][0])
    mid = get_mid(profiles[2], profiles[4])
    profiles[6] = process_line(profiles[6], foot, mid[0], mid[1])
    mid = get_mid(profiles[3], profiles[5])
    profiles[7] = process_line(profiles[7], foot, mid[0], mid[1])
    for profile in profiles:
        profile[:] = [round(meas * foot * 5) for meas in profile]
    return profiles

def get_min(height_map):
    minimum = 0
    for heights in map(list, height_map):
        min_now = min(heights)
        if min_now < minimum:
            minimum = min_now
    return minimum

def get_max(height_map):
    maximum = 0
    for heights in map(list, height_map):
        max_now = max(heights)
        if max_now > maximum:
            maximum = max_now
    return maximum

def get_flatness(height_map):
    minimum = 0
    maximum = 0
    for heights in map(list, height_map):
        min_now = min(heights)
        max_now = max(heights)
        if min_now < minimum:
            minimum = min_now
        if max_now > maximum:
            maximum = max_now
    return maximum - minimum


def grade(flat, grad):
    if flat <=  grad:
        return "AA"
    elif flat <=  grad * 2:
        return "A"
    elif flat <=  grad * 4:
        return "B"
    elif flat <=  grad * 8:
        return "C"
    else:
        return "TOOL"

def get_grade(flat, width, length):
    #   The procedure has a more extensive 
    #   list of standard plate sizes that
    #   conform to the "awkward_flatness"
    #   equation, so I have left them out.
    #   Here are those that do not conform:
    if width == 18 and length == 18:
        return grade(flat, 50)
    if width == 24 and length == 36:
        return grade(flat, 100)
    if width == 36 and length == 48:
        return grade(flat, 200)
    if width == 36 and length == 60:
        return grade(flat, 250)
    if width == 48 and length == 48:
        return grade(flat, 200)
    if width == 48 and length == 60:
        return grade(flat, 300)
    if width == 72 and length == 96:
        return grade(flat, 600)
    if width == 72 and length == 144:
        return grade(flat, 1100)
    awkward_flatness = (((int(width) ** 2) + (int(length) ** 2)) / 25) + 40
    awkward_flatness = round(awkward_flatness)
    mod = awkward_flatness % 25
    if mod < 12.5:
        awkward_flatness -= mod
    elif mod >= 12.5:
        awkward_flatness += 25 - mod
    awkward_flatness = grade(flat, awkward_flatness)
    return awkward_flatness

def get_closure(line):
    return line[round((len(line) - 1) / 2)]
           
            
profiles = [
    [1.32,0.90,0.10,-1.43,0.20,0.07,0.13,0.10,1.00,0.87,1.33,0.87,1.03,0.17,-0.23,0.63,0.23,0.17,],
    [2.50,2.37,2.50,1.87,3.40,3.33,2.77,3.33,3.57,3.83,4.57,3.93,4.67,3.77,3.80,4.53,3.93,3.63,],
    [4.43,4.53,3.83,3.00,3.67,4.60,4.50,5.30,4.93,5.17,6.17,5.50,6.20,6.87,6.33,5.20,],
    [7.80,7.97,7.50,6.70,6.77,7.20,6.50,5.37,],
    [5.73,5.40,5.00,4.67,6.07,6.00,6.80,7.17,7.17,7.83,8.40,8.17,8.00,8.17,7.50,6.57,],
    [-0.40,-1.47,-2.10,-1.60,-1.83,-2.00,-1.47,-1.63,],
    [11.93,11.40,10.10,9.57,9.23,8.23,9.47,9.13,],
    [8.93,8.47,7.37,6.23,7.57,7.60,7.77,8.23,8.53,8.43,8.87,8.23,8.17,8.07,7.13,7.00,],
]

flatness = get_height_map(profiles, foot = 4)
print(flatness)
height = get_flatness(flatness)
clos_7 = get_closure(profiles[6])
clos_8 = get_closure(profiles[7])
print(height)
print(get_grade(height, 36, 72))
print(str(clos_7) + " " + str(clos_8))