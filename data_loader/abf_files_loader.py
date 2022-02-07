# -*- coding: utf-8 -*-

from neo import io


def load_abf(filename):
    """
    Created on Tue Sep 11 10:52:17 2018
    extract the analog signal(s) from ABF files
    (generally acquired with clampex)
    @author: imbroscb
    """
    data = io.AxonIO(filename)
    b1 = data.read()[0]
    chan = {}
    for ch in range(len(b1.segments[0].analogsignals)):
        signal = []
        for s in range(len(b1.segments)):
            signal.append(b1.segments[s].analogsignals[0][:, ch])
            numb = ch + 1
        chan['ch%d'%numb] = signal
    return chan
