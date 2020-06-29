from unittest import TestCase
from pathlib import Path

import pandas as pd
from pandas.testing import assert_series_equal

import dynamotable

class ReadWriteDynamoTableTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.simple = Path().joinpath('test', 'data', 't_double.tbl')
        self.complex = Path().joinpath('test', 'data', 't_complex.tbl')
        self.tmap_complex = Path().joinpath('test', 'data', 'tmap_complex.doc')

    def test_open_simple(self):
        df = dynamotable.open(self.simple)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.columns[0] == 'tag')

    def test_open_complex(self):
        df = dynamotable.open(self.complex)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.columns[0] == 'tag')

    def test_open_complex_w_table_map(self):
        df = dynamotable.open(self.complex, self.tmap_complex)
        self.assertTrue('tomo_file' in df.columns)
        self.assertTrue(df['tomo_file'][0] == 'tomo_ts01.mrc_15.00Apx.mrc')

    def test_write_simple(self):
        df = dynamotable.open(self.simple)
        outfile = Path().joinpath('test', 'data', 'simple_out.tbl')

        dynamotable.write(df, outfile)
        df2 = dynamotable.open(outfile)

        for column in df.columns:
            assert_series_equal(df[column], df2[column], check_less_precise=True)

    def test_write_w_table_map(self):
        df = dynamotable.read(self.complex, self.tmap_complex)
        outfile = Path().joinpath('test', 'data', 'complex_out.tbl')

        dynamotable.write(df, outfile)

        tmap_file = str(outfile).replace('.tbl', '.doc')
        self.assertTrue(Path(tmap_file).exists())

        df2 = dynamotable.read(outfile, tmap_file)
        for column in df.columns:
            assert_series_equal(df[column], df2[column], check_less_precise=True)


