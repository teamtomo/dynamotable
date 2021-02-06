from pathlib import Path

import pandas as pd
from pandas.testing import assert_series_equal

import dynamotable

test_directory = Path(__file__).parent.absolute() / 'data'
simple_table = test_directory / 't_double.tbl'
complex_table = test_directory / 't_complex.tbl'
tomogram_table_map_complex = test_directory / 'tmap_complex.doc'


def test_open_simple():
    df = dynamotable.read(simple_table)
    assert isinstance(df, pd.DataFrame)
    assert df.columns[0] == 'tag'


def test_open_complex():
    df = dynamotable.read(complex_table)
    assert isinstance(df, pd.DataFrame)
    assert df.columns[0] == 'tag'


def test_open_complex_w_table_map():
    df = dynamotable.read(complex_table, tomogram_table_map_complex)
    assert 'tomo_file' in df.columns
    assert df['tomo_file'][0] == 'tomo_ts01.mrc_15.00Apx.mrc'


def test_write_simple():
    df = dynamotable.read(simple_table)
    file_out = Path().joinpath('test', 'data', 'simple_out.tbl')

    dynamotable.write(df, file_out)
    df2 = dynamotable.read(file_out)

    for column in df.columns:
        assert_series_equal(df[column], df2[column])


def test_write_w_table_map():
    df = dynamotable.read(complex_table, tomogram_table_map_complex)
    outfile = Path().joinpath('test', 'data', 'complex_out.tbl')

    dynamotable.write(df, outfile)

    tmap_file = str(outfile).replace('.tbl', '.doc')
    assert Path(tmap_file).exists()

    df2 = dynamotable.read(outfile, tmap_file)
    for column in df.columns:
        assert_series_equal(df[column], df2[column])
