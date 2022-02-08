# -*- coding: utf-8 -*-

import numpy as np


def load_txt(filename, datatype='float'):
    """
    Created on Wed Feb 13 14:43:47 2019

    load txt data of type 'float' and organized them in sweeps

    @author: imbroscb
    """
    if datatype == 'float':
        with open(filename) as f:
            temp = [line.split() for line in f]
            data = np.zeros((len(temp), len(temp[0])))
            for r in range(len(temp)):
                for c in range(len(temp[0])):
                    data[r, c] = float(temp[r][c])
    else:
        data = []
        with open(filename) as f:
            for line in f:
                data.append(line.strip())
    return data
