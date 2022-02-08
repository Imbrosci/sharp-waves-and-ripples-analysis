# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Gui_ripple_checker:
    """
    Created on Tue Sep 18 23:18:05 2018

    display the detected SWRs (raw signal, bandpass filtered signal,
    abs(Hilbert transformed signal) with the threshold for detection and offer
    the possibility to accept or reject the detected event.
    This Gui is initiated when the function SWR_detector is run with the option
    mode = 'manual'

    @author: imbroscb
    """

    def __init__(self, window, gap, threshold, cutout_raw, cutout_ripple,
                 cutout_env, fs, peak_time_manual, confirmed_peaktime,
                 data_length):
        self.window = window
        self.gap = gap
        self.threshold = threshold
        self.cutout_raw = cutout_raw
        self.cutout_ripple = cutout_ripple
        self.cutout_env = cutout_env
        self.fs = fs
        self.peak_time_manual = peak_time_manual
        self.confirmed_peaktime = confirmed_peaktime
        self.data_length = data_length
        self.plot()
        self.accept = tk.Button(self.window, text="accept", fg='green',
                                font=('Helvetica', '10'), command=self.accept)
        self.accept.pack(side=tk.LEFT)
        self.reject = tk.Button(self.window, text='reject', fg='red',
                                font=('Helvetica', '10'), command=self.reject)
        self.reject.pack(side=tk.LEFT)

    def plot(self):
        gap_ms = int(self.gap / (self.fs / 1000))
        if self.peak_time_manual < self.gap:
            time = np.linspace(int(-self.peak_time_manual / (self.fs/1000)),
                               gap_ms, int(self.cutout_raw.shape[0]))
            y_thr = np.linspace(self.threshold, self.threshold,
                                self.cutout_raw.shape[0])
        elif self.peak_time_manual + self.gap >= self.data_length:
            time = np.linspace(int(-self.peak_time_manual / (self.fs/1000)),
                               gap_ms, int(self.cutout_raw.shape[0]))
            y_thr = np.linspace(self.threshold, self.threshold,
                                self.cutout_raw.shape[0])
        else:
            time = np.linspace(-gap_ms, gap_ms,
                               int(gap_ms * 2 * (self.fs / 1000)))
            y_thr = np.linspace(self.threshold, self.threshold,
                                int(gap_ms * 2 * (self.fs / 1000)))

        fig = Figure(figsize=(10, 8))
        raw = fig.add_subplot(3, 1, 1)
        raw.plot(time, self.cutout_raw, color='black', label='raw_signal')
        raw.legend(loc='upper left')
        ripple = fig.add_subplot(3, 1, 2)
        ripple.plot(time, self.cutout_ripple, color='blue',
                    label='ripple_filtered_signal')
        ripple.legend(loc='upper left')
        env = fig.add_subplot(3, 1, 3)
        env.plot(time, self.cutout_env, color='orange',
                 label='Hilbert_transformed_signal')
        env.plot(time, y_thr)
        env.legend(loc='upper left')
        peak_time_sec = round(self.peak_time_manual / (self.fs), 2)

        fig.text(0.45, 0.03,
                 'Time of ripple peak in sec: {:.2f}'.format(peak_time_sec),
                 fontsize=20, ha='center')
        fig.text(0.04, 0.5, 'Amplitude (microV)', va='center',
                 rotation='vertical')
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (width, height))
        self.window.state('zoomed')
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        # canvas.show()
        # fig.text(0.5, 0.04, 'Time from ripple peak (ms)', ha='center')

    def accept(self):
        self.confirmed_peaktime = self.peak_time_manual
        self.window.quit()
        self.window.destroy()

    def reject(self):
        self.confirmed_peaktime = -1
        self.window.quit()
        self.window.destroy()
