# dynamotable
[![Build Status](https://travis-ci.com/alisterburt/dynamotable.svg?branch=master)](https://travis-ci.com/alisterburt/eulerangles)
[![PyPI version](https://badge.fury.io/py/dynamotable.svg)](https://pypi.org/project/dynamotable/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/dynamotable.svg)](https://pypi.python.org/pypi/dynamotable/)

`dynamotable` is a Python package to facilitate reading and writing of table files from the Dynamo subtomogram averaging package

## Features
- Read [table files](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Table) created by Dynamo as pandas DataFrames
- Write table files compatible with Dynamo subtomogram averaging from minimal data
- Supports reading and writing of [table map files](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Tomogram-table_map_file) with tables to keep track of tomogram files
- clean API



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
table map files are two column text files containing the tomogram index (found in column 20 of a table file) and the file path of the tomogram.
```
>>> df = dynamotable.read('t_complex.tbl', 'tmap_complex.doc')
>>> df
```
```
>>> df
        tag  aligned_value  ...  eig1                   tomo_file
0         2              1  ...     0  tomo_ts01.mrc_15.00Apx.mrc
1         4              1  ...     0  tomo_ts01.mrc_15.00Apx.mrc
2         6              1  ...     0  tomo_ts01.mrc_15.00Apx.mrc
3         8              1  ...     0  tomo_ts01.mrc_15.00Apx.mrc
4        10              1  ...     0  tomo_ts01.mrc_15.00Apx.mrc
     ...            ...  ...   ...                         ...
8737  18064              1  ...     0  tomo_ts99.mrc_15.00Apx.mrc
8738  18066              1  ...     0  tomo_ts99.mrc_15.00Apx.mrc
8739  18068              1  ...     0  tomo_ts99.mrc_15.00Apx.mrc
8740  18070              1  ...     0  tomo_ts99.mrc_15.00Apx.mrc
8741  18072              1  ...     0  tomo_ts99.mrc_15.00Apx.mrc

[8742 rows x 42 columns]
```
An extra column called `tomo_file` is added to the dataframe which contains the filepath of the tomogram you wish the particle to be linked to

### Writing table files
Table files are written with `dynamotable.write` or equivalently `dynamotable.new`
```python
>>> dynamotable.write(df, 'table_out.tbl')
```

Note that
- if `tag` is not a column in the dataframet then tags will be generated automatically
- if `tomo_file` is a column in the dataframe then a corresponding table map file will be generated
- if `tomo_file` is provided but no tomogram table indices are present these will be generated automatically
- if the `aligned_value` column is not present it will be set to 1 to mark particles for alignment in subtomogram averaging projects


## License
The project is released under the BSD 3-Clause License

## Known Issues
- 