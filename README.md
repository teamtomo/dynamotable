# dynamotable
[![Build Status](https://travis-ci.com/alisterburt/dynamotable.svg?branch=master)](https://travis-ci.com/alisterburt/eulerangles)
[![PyPI version](https://badge.fury.io/py/dynamotable.svg)](https://pypi.org/project/dynamotable/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/dynamotable.svg)](https://pypi.python.org/pypi/dynamotable/)

`dynamotable` is a Python package to facilitate reading and writing of table files from the Dynamo subtomogram averaging package

## Features
- Read and write table files created by Dynamo as pandas DataFrames
- Support for streamlined table map file reading and writing



## Installation
Installation is available directly from the [Python package index](https://pypi.org/project/dynamotable/)
```
pip install dynamotable
```

## Usage

### Reading table files
#### Simple
```python
import dynamotable
df = dynamotable.open('t_double.tbl')
```
```
>>> df = dynamotable.open('t_double.tbl')
>>> df
     tag  aligned_value  averaged_value        dx  ...  npar  undefined1  ref  sref
0      1              1               0  2.517800  ...     0           0    0     5
1      2              1               0  3.246300  ...     0           0    0     4
2      3              1               0 -2.984100  ...     0           0    0     4
3      4              1               0  3.307000  ...     0           0    0     4
4      5              1               0  1.058900  ...     0           0    0     2
..   ...            ...             ...       ...  ...   ...         ...  ...   ...
295  296              1               0 -2.656600  ...     0           0    0     5
296  297              1               0  3.829400  ...     0           0    0     1
297  298              1               0  1.701600  ...     0           0    0     5
298  299              1               0  0.003773  ...     0           0    0     2
299  300              1               0 -0.231290  ...     0           0    0     3

[300 rows x 35 columns]
```

#### With table map file

### Writing table files


## License
The project is released under the BSD 3-Clause License

## Known Issues
- 