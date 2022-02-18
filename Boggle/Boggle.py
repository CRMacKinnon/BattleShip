import pandas as pd
import os
import sys
import random
import numpy as np


def Shake_Boggle(dice_list):
    '''
    Generates a new Boggle instace
    '''
    sides = ''
    Letter_list = []
    for dice in dice_list:
        sides += dice
        if len(sides) % 6 == 0:
            Role = sides[random.randint(0, 5)]
            Letter_list.append(Role)
            sides = ''
    print(np.asarray(Letter_list).reshape(4, 4))
    return Letter_list


dir = os.path.dirname(sys.argv[0]) + '/'

word_list_master = pd.read_csv(dir + 'reduced_dictionary.txt',
                               header=0, sep='\t', keep_default_na=False)
word_list = word_list_master['Words'].values.tolist()

new_boggle = list(
    'AAEEGNABBJOOACHOPSAFFKPSAOOTTWCIMOTUDEILRXDELRVYDISTTYEEGHNWEEINSUEHRTVWEIOSSTELRTTYHIMNUQHLNNRZ'.lower())

_BOGGLE = Shake_Boggle(new_boggle)
_BOGGLE_DICT = {}


'''Boggle Index
0  1  2  3
4  5  6  7
8  9  10 11
12 13 14 15
'''

_DICE_NEIGHBOURS = {0: [1, 4, 5],
                    1: [0, 2, 4, 5, 6],
                    2: [1, 3, 5, 6, 7],
                    3: [2, 6, 7],
                    4: [0, 1, 5, 8, 9],
                    5: [0, 1, 2, 4, 6, 8, 9, 10],
                    6: [1, 2, 3, 5, 7, 9, 10, 11],
                    7: [2, 3, 6, 10, 11],
                    8: [4, 5, 9, 12, 13],
                    9: [4, 5, 6, 8, 10, 12, 13, 14],
                    10: [5, 6, 7, 9, 11, 13, 14, 15],
                    11: [6, 7, 10, 14, 15],
                    12: [8, 9, 13],
                    13: [8, 9, 10, 12, 14],
                    14: [9, 10, 11, 13, 15],
                    15: [10, 11, 14]}

for ID in _BOGGLE_DICT:
    if 'q' in ID[0]:
        _BOGGLE_DICT['q'] = _BOGGLE_DICT.pop('qu')

for idx, dice in enumerate(_BOGGLE):
    _BOGGLE_DICT[dice+str(idx)] = 1

_INSTANCE_DICTIONARY = {}

for dice in _BOGGLE_DICT:
    for word in word_list:
        if dice[0] == word[0]:
            if dice[0] not in _INSTANCE_DICTIONARY:
                _INSTANCE_DICTIONARY[dice[0]] = []
            _INSTANCE_DICTIONARY[dice[0]].append(word)
