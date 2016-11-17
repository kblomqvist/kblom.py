# kblom.py
![Python3](https://img.shields.io/badge/python-3-green.svg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/kblomqvist/kblom.py/blob/master/LICENSE)

## Installation (editable)
```bash
git clone https://github.com/kblomqvist/kblom.py.git
pip3 install -e kblom.py
```

### Update library
```bash
cd kblom.py
git pull
```

## Timeseries

### Rolling window (aka sliding window)

Built-in rolling window filters:
- `RollingMean`
- `RollingMedian`
- `RollingRootMeanSquare`

You can create your own rolling window by inheriting from `ts.RollingWindow`, e.g. rolling median filter has been implemented like this

```python
from kblom.dsp import timeseries as ts

class RollingMedian(ts.RollingWindow):

    def window_operation(self, window):
        return np.median(window)
```

and it would be used like this

```python
median = RollingMedian(window_len=0.1, fs=175)  # window_len is in seconds and fs in Hz
x = range(100)
y = list(sma.roll(x, end=True))                 # roll() returns a generator
```

Window length can also be given in integer instead of seconds. Just omit the `fs`, but make sure that your window length is an odd number. That's because the output signal will be delayled by (N-1)/2. Additionally, if you like to use the rolling window for real-time signals you can make consecutive calls to `roll()`.
