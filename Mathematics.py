"""
Copyright (C) 2019  Kropf Simon

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details. 

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import matplotlib
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import collections
import numpy

CHARACTER_MAP = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
    9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G',
    17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O',
    25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W',
    33: 'X', 34: 'Y', 35: 'Z'
}
HEBREW_ALPHABET = {
    1: ['alef', '\u05D0', ''], 2: ['bet', '\u05D1', 'B'], 3: ['gimel', '\u05D2', 'G'],
    4: ['dalet', '\u05D3', 'D'], 5: ['he', '\u05D4', 'H'], 6: ['vav', '\u05D5', 'V'],
    7: ['zayin', '\u05D6', 'Z'], 8: ['het', '\u05D7', 'H'], 9: ['tet', '\u05D8', 'T'],
    10: ['yud', '\u05D9', 'Y'], 20: ['kaf', '\u05DB', 'K'], 30: ['lamed', '\u05DC', 'L'],
    40: ['mem', '\u05DE', 'M'], 50: ['nun', '\u05E0', 'N'], 60: ['samekh', '\u05E1', 'S'],
    70: ['ayin', '\u05E2', ''], 80: ['pe', '\u05E4', 'P'],  90: ['tsadi', '\u05E6', 'TS'],
    100: ['kuf', '\u05E7', 'K'], 200: ['resh', '\u05E8', 'R'],
    300: ['shin', '\u05E9', 'SH'], 400: ['tav', '\u05EA', 'T']
}
HEBREW_ALPHABET_FINALS = {
    20: ['final kaf', '\u05DA'], 40: ['final mem', '\u05DD'],
    50: ['final nun', '\u05DF'], 80: ['final pe', '\u05E3'],
    90: ['final tsadi', '\u05E5']
}


# Creates a generator for a doubling sequence in any base
def get_doubling_sequence(start, base):
    while True:
        yield convert_decimal_to_base(start, base)
        start = start * 2

# Converts a decimal number to any base
# uses recursion for conversion
# parameter converted !not! used when calling this function (used for recursion part)
def convert_decimal_to_base(number, base, converted=''):
    if number:
        if 2 <= base <= 36:
            return convert_decimal_to_base(int(number / base), base, CHARACTER_MAP[number % base] + converted)
        else:
            return convert_decimal_to_base(int(number / base), base, str(number % base) + '.' + converted if converted else str(number % base))
    return converted


# Converts a number from any base to decimal base
# uses recursion for conversion
# parameters converted & power are !not! used when calling this function (there here for the recursion part)
def convert_base_to_decimal(number, base, converted=0, power=0):
    number = str(number)
    if number:
        if 2 <= base <= 36:
            return convert_base_to_decimal(number[:-1], base, converted + list(CHARACTER_MAP.values()).index(number[-1]) * (base ** power), power + 1)
        else:
            return convert_base_to_decimal('.'.join(number.split('.')[:-1]), base, converted + int(number.split('.')[-1]) * (base ** power), power + 1)
    return converted


# Calculates the digital root of any number with any base
# also uses recursion
def get_digital_root(number, base):
    if convert_base_to_decimal(number, base) >= base:
        if 2 <= base <= 36:
            return get_digital_root(convert_decimal_to_base(sum([list(CHARACTER_MAP.values()).index(elem) for elem in list(str(number))]), base), base)
        else:
            return get_digital_root(convert_decimal_to_base(sum([int(elem) for elem in str(number).split('.')]), base), base)
    return number