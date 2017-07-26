
# Copyright (C) 2016  Kropf Simon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import matplotlib
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import collections
import numpy



character_map = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
    9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G',
    17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O',
    25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W',
    33: 'X', 34: 'Y', 35: 'Z'
}
character_map_rev = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
    '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16,
    'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24,
    'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32,
    'X': 33, 'Y': 34, 'Z': 35
}
hebrew_alphabet = {
    1: ['alef', '\u05D0', ''], 2: ['bet', '\u05D1', 'B'], 3: ['gimel', '\u05D2', 'G'],
    4: ['dalet', '\u05D3', 'D'], 5: ['he', '\u05D4', 'H'], 6: ['vav', '\u05D5', 'V'],
    7: ['zayin', '\u05D6', 'Z'], 8: ['het', '\u05D7', 'H'], 9: ['tet', '\u05D8', 'T'],
    10: ['yud', '\u05D9', 'Y'], 20: ['kaf', '\u05DB', 'K'], 30: ['lamed', '\u05DC', 'L'],
    40: ['mem', '\u05DE', 'M'], 50: ['nun', '\u05E0', 'N'], 60: ['samekh', '\u05E1', 'S'],
    70: ['ayin', '\u05E2', ''], 80: ['pe', '\u05E4', 'P'],  90: ['tsadi', '\u05E6', 'TS'],
    100: ['kuf', '\u05E7', 'K'], 200: ['resh', '\u05E8', 'R'],
    300: ['shin', '\u05E9', 'SH'], 400: ['tav', '\u05EA', 'T']
}
hebrew_alphabet_finals = {
    20: ['final kaf', '\u05DA'], 40: ['final mem', '\u05DD'],
    50: ['final nun', '\u05DF'], 80: ['final pe', '\u05E3'],
    90: ['final tsadi', '\u05E5']
}


def get_doubling_sequence(start, iterations, base):
    list = []
    while iterations:
        list.append(convert_number_to_base(start, base))
        iterations = iterations - 1
        start = start * 2
    return list


def __convert_decimal_number_to_base__(number, base):
    if base <= 10:
        buffer = []
        while number:
            buffer.append(str(number % base))
            number = int(int(number) / int(base))
        return ''.join(buffer[::-1])
    elif base <= 36:
        buffer = []
        while number:
            rest = number % base
            if rest >= 10:
                buffer.append(character_map[rest])
            else:
                buffer.append(str(rest))

            number = int(int(number) / int(base))

        return ''.join(buffer[::-1])
    else:
        buffer = []
        while number:
            buffer.insert(0, str(number % base))
            number = int(int(number) / int(base))
            buffer.insert(0, '.')
        return ''.join(buffer[1::1])


def convert_to_base(number, number_base, target_base):
    if number_base == target_base: return number
    if number_base == 10:
        return __convert_decimal_number_to_base__(number, target_base)
    if number_base <= 36:
        result = 0
        buffer = list(str(number))
        base_buffer = 1
        while len(buffer) != 0:
            result = result + int(character_map_rev[buffer.pop()]) * base_buffer
            base_buffer = base_buffer * number_base
        return __convert_decimal_number_to_base__(result, target_base)
    else:
        result = 0
        buffer = str(number).split('.')
        base_buffer = 1
        while len(buffer) != 0:
            result = result + int(buffer.pop()) * base_buffer
            base_buffer = base_buffer * number_base
        return __convert_decimal_number_to_base__(result, target_base)


def get_digital_root(number, base):
    number = int(convert_to_base(number, base, 10))
    while number >= 10:
        buffer = list(str(number))
        number = 0
        for digit in buffer:
            number = number + int(digit)
    return number


def __init__(self):
    pyramid = get_fibonacci_pyramid(5)

    print(get_fibonacci_sequence(0, 10))
    for level in pyramid:
        print(level)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xlist = []
    ylist = []
    zlist = []
    data = []

    xlist.append(0.0)
    ylist.append(0.0)
    zlist.append(0.0)

    indentStep = 2

    for level in range(2, pyramid.maxlen + 1):
        for i in range(level):
            for j in range(level):

                if level % 2 == 1:
                    center = math.floor(level / 2)
                if level % 2 == 0:
                    center = (level / 2) - 0.5

                xlist.append((i - center) * indentStep)
                ylist.append((j - center) * indentStep)
                zlist.append(level - 1)

    for level in range(pyramid.maxlen):
        for i in range(level + 1):
            for j in range(level + 1):
                data.append(pyramid[level][i][j])

    ax.scatter(xlist, ylist, zlist, zdir='z', marker=None)

    i = 0
    for x, y, z in zip(xlist, ylist, zlist):
        ax.text(x, y, z, str(data[i]), color="red", fontsize=8)
        i = i + 1

    plt.show()

__init__(0)
# for i in range(0, 10):
#     result = []
#     for item in m.get_fibonacci_sequence(i*24, i*24+24):
#         result.append(m.get_digit_sum(item, 10))
#     print(result)
# mathematics.print_hebrew()

# result = []
# fib = m.get_fibonacci_sequence(0,24)
# for number in fib:
#     convNumber = m.convert_number_to_base(number, 16)
#     result.append(convNumber)
# print(result)

#for item in hebrew_alphabet:
#    print(hebrew_alphabet[item][1] + ':    ' + hebrew_alphabet[item][0] + '\t' + hebrew_alphabet[item][2])
