# -*- coding: utf-8 -*-

import numpy as np


def get_channels(chan, position, fs):
    """
    Created on Tue Sep 11 14:30:48 2018

    inputs:
        chan  = the data organized as a dictionary obtained with the function
                loading_abf
        position = a list with the names of the recording location
        fs = the sampling rate (Hz)
    output:
        data = as chan but with the names of the recording locations as key

    @author: imbroscb
            """
    data = {}
    c = 0
    for key, value in chan.items():
        data[position[c]] = np.asarray(value).reshape(-1, 1)
        c += 1

    return data
