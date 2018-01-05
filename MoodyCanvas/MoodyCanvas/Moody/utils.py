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

