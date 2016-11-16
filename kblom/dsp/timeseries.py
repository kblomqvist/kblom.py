"""
The MIT License (MIT)

Copyright (c) 2016 Kim Blomqvist

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from abc import ABC, abstractmethod

import numpy as np


class RollingWindow(ABC):
    """Abstract rolling window to be inherited by filter classes.

    Note!  The implementation will delay subsamples by (N-1)/2,
    where N is the length of the window.

    Keyword arguments:
        window_len (int|double): Window length as an integer or in seconds
                                 if fs is given.
        fs (int|double): Sampling frequency in Hz. (Optional)
    """

    def __init__(self, window_len, fs=None):
        if fs is not None:
            window_len = np.int(fs * window_len)
            if not window_len % 2:
                window_len += 1

        assert window_len % 2   # (N-1)/2 has to be integer

        self.window = []
        self.window_len = window_len
        self.window_delay = np.int((window_len-1)/2)

    def roll(self, vector, end=False):
        """Returns a generator for the rolling window subsamples.

        Multiple calls will remember the previous state so you can call
        roll() in real-time for chucks of data.  Calling sample-by-sample is
        also possible when the vector is a single value list.  To stop
        the analysis define end=True.  This would also allow a static
        analysis, e.g.

            sma = RollingMean(0.1, fs=175)
            y = list(sma.roll(x, end=True))  # len(y) == len(x)

        Keyword arguments:
            vector (list): Chunk of samples.
            end (bool): True will "reset" the class.
        """
        for sample in vector:
            self.window_append(sample)
            if len(self.window) > self.window_len:
                self.window.pop(0)
            if len(self.window) > self.window_delay:
                yield self.window_operation(self.window)

        if end:
            while len(self.window) > self.window_delay + 1:
                self.window.pop(0)
                yield self.window_operation(self.window)
            self.window[:] = []

    @abstractmethod
    def window_operation(self, window):
        """Implement this to calculate result for window subsample.
        
        Keyword arguments:
            window (list): The current window of samples.
        """
        pass

    def window_append(self, sample):
        """Override to modify sample before it's appended to window."""
        self.window.append(sample)


class RollingMean(RollingWindow):
    """Rolling mean aka. simple moving average (SMA) filter."""

    def __init__(self, window_len, fs=None):
        self.sum = None
        RollingWindow.__init__(self, window_len, fs)

    def roll(self, vector, end=False):
        for result in RollingWindow.roll(self, vector, end):
            yield result
        if end:
            self.sum = None

    def window_operation(self, window):
        """A simple solution would have been 'return np.mean(window)',
        but it would had a bad performance.  The below solution avoids
        multiple calculations of the same thing, i.e. when calculating
        successive values, a new value comes into the sum and an old value
        drops out, meaning a full summation each time is unnecessary for
        this simple case.
        """
        if self.sum is None:
            self.sum = np.sum(window)
            self.prev_window_len = len(window)
            return self.sum / len(window)

        if self.prev_window_len <= len(window):
            self.sum += window[-1]
        result = self.sum / len(window)

        if len(window) in [self.window_len, self.prev_window_len-1]:
            self.sum -= window[0]  # Remove the latest sample from next roll

        self.prev_window_len = len(window)
        return result


class RollingRootMeanSquare(RollingMean):
    """Rolling RMS filter."""

    def window_append(self, sample):
        self.window.append(sample**2)  # Avoid unnecessary calculation of ^2

    def window_operation(self, window):
        result = RollingMean.window_operation(self, window)
        return np.sqrt(result)


class RollingMedian(RollingWindow):
    """Rolling median filter."""

    def window_operation(self, window):
        return np.median(window)
