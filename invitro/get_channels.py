# -*- coding: utf-8 -*-

import numpy as np


def get_channels(chan, position, fs):
    """
    Created on Tue Sep 11 14:30:48 2018
    input parameters:
        chan  = the data organized as a dictionary obtained with the function
                loading_abf
        position = a list with the names of the recording location
        fs = the sampling rate (Hz)
    outputs:
        raw_data = as chan but with the names of the recording locations as key
        proc_data = data after 50Hz noise subctraction
    @author: imbroscb
            """
    raw_data = {}
    proc_data = {}
    c = 0
    for key, value in chan.items():
        temp_list = []
        # the following for loop is necessary for 50Hz noise subtraction
        for sw in range(len(chan[key])):
            template = np.tile(value[sw][:400], (int(len(value[sw]) / 400), 1))
            temp_list.append(np.asarray(value[sw]) - np.array(template))
        raw_data[position[c]] = np.asarray(value).reshape(-1, 1)
        proc_data[position[c]] = np.asarray(temp_list).reshape(-1, 1)
        c += 1
    return raw_data, proc_data