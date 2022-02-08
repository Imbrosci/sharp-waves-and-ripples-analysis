# -*- coding: utf-8 -*-

import numpy as np
from scipy import signal
import tkinter as tk

# custom scripts
from invitro.gui_ripple_checker import Gui_ripple_checker
from signal_processing.butter import bandpass


def SWR_detector(raw_data, thr, fs=20000, low=150, high=300, cutout_width=None,
                 mode='auto'):
    """
    Created on Fri Sep  7 00:50:24 2018

    inputs:
        raw_data = it should be organized as a vector, if there are more sweeps
        they should be concatenated.
        fs = sampling rate (in Hz), default = 20000
        thr = times the std of the ripplepass signal from baseline
        low = low edge of frequency band  to use (in Hz), default = 150
        high = high edge of frequency band to use (in Hz), default = 300
        cutout_width = length of cutout to be displayed in ms, default = 400.
                       this means that a chunk of +- 200 ms from ripple peak
                       are displayed.
        mode = 'auto' or 'manual'. if 'manual' is selected each detected SWR is
               displayed and the user can decide if to accept or reject it,
               default='auto'

    output:
        peak_times = in datapoints, not in ms (peak times of the hilbert
                     transformation of the ripplepass signal for each detected
                     SWR)

    @author: imbroscb
    """
    if (mode != 'auto') and (mode != 'manual'):
        raise ValueError('mode should be set to either auto or manual')
    if cutout_width is None:
        gap = int((fs / 10) * 2)
    else:
        gap = int(cutout_width * fs / 1000 / 2)

    # bandpass the signal
    ripplepass_signal = bandpass(raw_data, low, high, fs)

    # hilbert transformation
    ripple_env = np.abs(signal.hilbert(ripplepass_signal, axis=0))

    # calculate the threshold th times the std of signal
    base_var = np.std(ripplepass_signal)
    threshold = base_var*thr

    # look for timestamp when signal is above threshold
    peak_time_pre = []
    peak_amp_env = []

    for i in range(len(ripple_env) - 2):
        perc = (i / (len(ripple_env) - 2)) * 100
        print('first screening: {:.2f} % done'.format(perc))
        if ripple_env[i] > threshold:
            peak_time_pre.append(i+1)
            peak_amp_env.append(ripple_env[i+1])

    # the piece of code below eliminates multiple peaks belonging to the same
    # event and keep only one datapoint at max amplitude
    c = 0  # c stays for current
    peak_time_auto = []
    peak_times = []
    while c < (len(peak_time_pre)):
        perc = (c / len(peak_time_pre)) * 100
        print('optimization: {:.2f} % done'.format(perc))

        t = 1  # t stays for next
        temp = c

        # test if there are more peaks within a refractory period of 200 ms
        delta = peak_time_pre[c+t]-peak_time_pre[c]
        while delta < 200*(fs/1000):
            temp = int(c + t)
            t += 1
            if c + t >= len(peak_time_pre):
                delta = 200 * (fs / 1000) + 1
            else:
                delta = peak_time_pre[c + t] - peak_time_pre[c]

        # if more than 1 peak_time was found within 200 ms choose the
        # biggest and append it to peak_time
        if temp > c:
            temp_argmax = np.argmax(peak_amp_env[c:temp + 1])
            peak_time_auto.append(peak_time_pre[c + temp_argmax])
            peak_time_manual = peak_time_pre[c + temp_argmax]
        else:
            peak_time_auto.append(peak_time_pre[temp])
            peak_time_manual = peak_time_pre[temp]

        c = c + t

        if mode == 'manual':
            if peak_time_manual < gap:
                cutout_raw = raw_data[:peak_time_manual + gap]
                cutout_ripple = ripplepass_signal[:peak_time_manual + gap]
                cutout_env = ripple_env[:peak_time_manual + gap]
            elif peak_time_manual + gap >= raw_data.shape[0]:
                cutout_raw = raw_data[peak_time_manual - gap:]
                cutout_ripple = ripplepass_signal[peak_time_manual - gap:]
                cutout_env = ripple_env[peak_time_manual - gap:]
            else:
                cutout_raw = raw_data[peak_time_manual - gap:
                                      peak_time_manual + gap]
                cutout_ripple = ripplepass_signal[peak_time_manual - gap:
                                                  peak_time_manual + gap]
                cutout_env = ripple_env[peak_time_manual - gap:
                                        peak_time_manual + gap]
            confirmed_peaktime = -1
            data_length = raw_data.shape[0]
            window = tk.Tk()
            # class instantiation
            start = Gui_ripple_checker(window, gap, threshold, cutout_raw,
                                       cutout_ripple, cutout_env, fs,
                                       peak_time_manual, confirmed_peaktime,
                                       data_length)
            window.mainloop()
            if start.confirmed_peaktime != -1:
                peak_times.append(peak_time_manual)

    if mode == 'auto':
        peak_times = peak_time_auto

    return peak_times
