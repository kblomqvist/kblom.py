# kblom.py

```bash
pip install -e https://github.com/kblomqvist/kblom.py.git
```

```ipython
>>> from kblom.dsp import timeseries as ts
>>> sma = ts.RollingMean(0.1, fs=175)
>>> x = range(100)
>>> y = list(sma.roll(x, end=True))
>>> assert len(x) is len(y)
```
