import collections
import numpy as np
import math
import itertools as it

def get_fibonacci_number(position):
    return get_fibonacci_sequence(0, position)[position - 1]

def get_fibonacci_sequence(start, end):
    sequence = [1, 1]
    end = end - 2

    for i in range(end):
        sequence.append(sequence[-1] + sequence[-2])

    return sequence[start:]

def get_fibonacci_pyramid(level):
    pyramid = collections.deque(maxlen=level)

    for i in range(1, level + 1):
        zeros = np.zeros(shape=(i, i), dtype=int)
        pyramid.append(zeros)

    pyramid[0][0][0] = 1
    pyramid[1][0][0] = 1
    pyramid[1][1][0] = 1
    pyramid[1][0][1] = 1
    pyramid[1][1][1] = 1

    _iterate_pyramid_(pyramid, 2)

    return pyramid

def _iterate_pyramid_(pyramid, currentLevel):
    if pyramid.maxlen <= currentLevel: return pyramid

    for i in range(currentLevel + 1):
        for j in range(currentLevel + 1):
            # Calculating four corners of current level
            # Extra note: Don't change order of if-statements
            # because 'var j' is processed first!
            if j == 0 and i == 0:
                pyramid[currentLevel][i][j] = pyramid[currentLevel - 1][i][j] + pyramid[currentLevel - 2][i][j]
                continue
            if j == 0 and i == currentLevel:
                pyramid[currentLevel][i][j] = pyramid[currentLevel - 1][i - 1][j] + pyramid[currentLevel - 2][i - 2][j]
                continue
            if j == currentLevel and i == 0:
                pyramid[currentLevel][i][j] = pyramid[currentLevel - 1][i][j - 1] + pyramid[currentLevel - 2][i][j - 2]
                continue
            if j == currentLevel and i == currentLevel:
                pyramid[currentLevel][i][j] = pyramid[currentLevel - 1][i - 1][j - 1] + pyramid[currentLevel - 2][i - 2][j - 2]
                continue

            # Calculating four edges of current level
            # Extra note: Same here. Don't change order of the if-statements
            if j == 0:
                pyramid[currentLevel][i][j] = pyramid[currentLevel - 1][i - 1][j] + pyramid[currentLevel - 1][i][j]
                continue
            if i == 0:
                pyramid[currentLevel][i][j] = pyramid[currentLevel - 1][i][j - 1] + pyramid[currentLevel - 1][i][j]
                continue
            if j == currentLevel:
                pyramid[currentLevel][i][j] = pyramid[currentLevel - 1][i - 1][j - 1] + pyramid[currentLevel - 1][i][j - 1]
                continue
            if i == currentLevel:
                pyramid[currentLevel][i][j] = pyramid[currentLevel - 1][i - 1][j - 1] + pyramid[currentLevel - 1][i - 1][j]
                continue

            # Calculating inner area of current level
            pyramid[currentLevel][i][j] = pyramid[currentLevel - 1][i - 1][j - 1] + pyramid[currentLevel - 1][i - 1][j] + pyramid[currentLevel - 1][i][j - 1] + pyramid[currentLevel - 1][i][j]

    _iterate_pyramid_(pyramid, currentLevel + 1)

def _get_fibonacci_correction_list(level, orientation):
    # correction x,y values
    # for right-turning spirals
    # switch xList & yList for left-turning spirals
    # xList=[0, 0, 0, 1,  1, -2.0, -2.0, 6.0,  6.0, -15.0, -15.0, 40.0,  40.0, -104.0, -104.0]
    # yList=[0, 0, 1, 1, -1, -1.0,  4.0, 4.0, -9.0,  -9.0,  25.0, 25.0, -64.0,  -64.0,  169.0]
    xList = [0, 0, 0, 1, 1]
    yList = [0, 0, 1, 1, 1, 1]

    for i in range(5, level, 2):
        # The last four elements in the list are added and the fifth last is subtracted = this is the value for the next two elements
        x = xList[i - 1] + xList[i - 2] + xList[i - 3] + xList[i - 4] - xList[i - 5]
        xList.append(x)
        xList.append(x)
        # The last four elements in the list are added and the fifth last is subtracted = this is the value for the next two elements
        y = yList[i] + yList[i - 1] + yList[i - 2] + yList[i - 3] - yList[i - 4]
        yList.append(y)
        yList.append(y)

    # change algebraic sign accordingly
    # as you can see in the examples above you always have 2 negative then 2 positive and so on
    # in x and y direction these signs are shifted to each other (expressed in these startX/Y vars below)
    startX = 1
    startY = 0
    for i in range(startX, len(xList), 4):
        # negiative sign for the next two elements (if existing => no OOB Exception)
        xList[i] = xList[i] * -1
        if len(xList) > i + 1: xList[i + 1] = xList[i + 1] * -1
    for i in range(startY, len(yList), 4):
        # negiative sign for the next two elements (if existing => no OOB Exception)
        yList[i] = yList[i] * -1
        if len(yList) > i + 1: yList[i + 1] = yList[i + 1] * -1

    # switch lists if orientation is left
    if orientation == 'l': correctionList = { 'x': yList, 'y': xList }
    else: correctionList = { 'x': xList, 'y': yList }

    return correctionList

def get_fibonacci_spiral(level, rotAngle = [0, 0, 0], orientation = 'r', zFactor = 0, segments=16):
    fib_seq = get_fibonacci_sequence(0, level)

    correctionList = _get_fibonacci_correction_list(level, orientation)

    data = []
    angle = 0
    counter = 0
    zPosNext = 0
    for fib in fib_seq:
        #set starting and ending z-Position for spatial positioning
        zPos = zPosNext
        zPosNext = zPos + (fib / 100.0 * zFactor)

        #set x&y lists with sine and r=fib to get circular quarter sections
        x = fib * np.sin(np.linspace(np.pi / 2, np.pi, segments))
        y = fib * np.sin(np.linspace(0, np.pi / 2, segments)) 

        #rotate the fib-quarter-circle section accordingly to orientation
        if orientation == 'r':
            z = list(reversed(np.linspace(zPos, zPosNext, segments)))
            rotated_matrix = _rot_matrix_(np.matrix([x, y, z]), 'z', angle)
        elif orientation == 'l':
            z = list(np.linspace(zPos, zPosNext, segments))
            rotated_matrix = _rot_matrix_(np.matrix([x, y, z]), 'z', -angle)

        #set lists with offset correction
        x = [x + correctionList['x'][counter] for x in rotated_matrix[0]]
        y = [y + correctionList['y'][counter] for y in rotated_matrix[1]]
        z = rotated_matrix[2]

        rotMatrix = [x, y, z]

        #rotate finished fibonacci section again if desired (=rotAngle)
        if rotAngle[2] != 0: rotMatrix = _rot_matrix_(np.matrix(rotMatrix), 'z', rotAngle[2])
        if rotAngle[1] != 0: rotMatrix = _rot_matrix_(np.matrix(rotMatrix), 'y', rotAngle[1])
        if rotAngle[0] != 0: rotMatrix = _rot_matrix_(np.matrix(rotMatrix), 'x', rotAngle[0])

        #append finished matrix to the data list
        data.append(rotMatrix)

        #add 90deg to angle (=> next section)
        #counter for appropriate position in offset list (xList, yList)
        angle = angle + math.pi / 2
        counter = counter + 1

    # converting the data which has 3 lists of x, y & z coordinates
    # into one list with [x,y,z] points
    points = []
    for section in data:
        pos = []
        for x, y, z in zip(section[0], section[1], section[2]):
            pos.append([round(x, 2), round(y, 2), round(z, 2)])
        
        if orientation == 'r': points.extend(reversed(pos))
        if orientation == 'l': points.extend(pos)

    return points

def get_fibonacci_cubes(level, rotAngle = [0, 0, 0], orientation = 'r', zFactor = 0):
    fib_seq = get_fibonacci_sequence(0, level)

    correctionList = _get_fibonacci_correction_list(level, orientation)
    xList = correctionList[0]
    yList = correctionList[1]

    cubes = []
    angle = 0
    counter = 0
    zPosNext = 0
    for fib in fib_seq:
        #set starting and ending z-Position for spatial positioning
        zPos = zPosNext
        zPosNext = zPos + (fib / 100.0 * zFactor)

        #creation of cube (12 lines for each edge)
        cube = []
        r = [0, fib]
        for s, e in it.combinations(np.array(list(i.product(r,r,r))), 2):
            if np.sum(np.abs(s-e)) == r[1]-r[0]:
                line = list(zip(s,e))
                #correct z-Values to fit height (zFactor)
                line[2] = (line[2][0] / 100.0 * zFactor + zPos, line[2][1] / 100.0 * zFactor + zPos)
                #rotate the cube accordingly to orientation
                if orientation == 'r':
                    rotated_line = _rot_matrix_(np.matrix(line), 'z', angle)
                elif orientation == 'l':
                    rotated_line = _rot_matrix_(np.matrix(line), 'z', -angle)

                #set lists with offset correction
                x = [x + xList[counter] for x in rotated_line[0]]
                y = [y + yList[counter] for y in rotated_line[1]]
                z = rotated_line[2]

                rotLine = [x, y, z]

                #rotate finished fibonacci section again if desired (=rotAngle)
                if rotAngle[2] != 0: rotLine = _rot_matrix_(np.matrix(rotLine), 'z', rotAngle[2])
                if rotAngle[1] != 0: rotLine = _rot_matrix_(np.matrix(rotLine), 'y', rotAngle[1])
                if rotAngle[0] != 0: rotLine = _rot_matrix_(np.matrix(rotLine), 'x', rotAngle[0])

                cube.append(rotLine)

        # add 90deg to angle (=> next section)
        # counter for appropriate position in offset list (xList, yList)
        angle = angle + math.pi / 2
        counter = counter + 1


        cubes.append(cube)

    return cubes

# Matrix rotation
# website for matrix operations: http://inside.mines.edu/fs_home/gmurray/ArbitraryAxisRotation/
def _rot_matrix_(matrix, axis, angle):
    if axis == 'x':
        x = np.array([1, 0, 0])
        y = np.array([0, np.cos(angle), -np.sin(angle)])
        z = np.array([0, np.sin(angle), np.cos(angle)])
    elif axis == 'y':
        x = np.array([np.cos(angle), 0, np.sin(angle)])
        y = np.array([0, 1, 0])
        z = np.array([-np.sin(angle), 0, np.cos(angle)])
    elif axis == 'z':
        x = np.array([np.cos(angle), -np.sin(angle), 0])
        y = np.array([np.sin(angle), np.cos(angle), 0])
        z = np.array([0, 0, 1])
    return np.array((matrix.getT() * np.matrix([x,y,z])).getT()).tolist()
