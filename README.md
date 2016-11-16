# kblom.py
[![Python3](https://img.shields.io/badge/python-3-green.svg)
![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/kblomqvist/kblom.py/blob/master/LICENSE)


```bash
pip3 install -e https://github.com/kblomqvist/kblom.py.git
```

```python
>>> from kblom.dsp import timeseries as ts
>>> sma = ts.RollingMean(0.1, fs=175)
>>> x = range(100)
>>> y = list(sma.roll(x, end=True))
>>> assert len(x) is len(y)
```
