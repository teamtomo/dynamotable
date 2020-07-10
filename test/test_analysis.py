from unittest import TestCase
from pathlib import Path

import dynamotable


class AnalysisTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.simple = Path().joinpath('test', 'data', 't_double.tbl')
        self.complex = Path().joinpath('test', 'data', 't_complex.tbl')
        self.tmap_complex = Path().joinpath('test', 'data', 'tmap_complex.doc')

    def test_xyz(self):
        df = dynamotable.open(self.simple)
        xyz = dynamotable.xyz(df)
        self.assertTrue(xyz.shape[0] == 300)
        self.assertTrue(xyz.shape[1] == 3)

    def test_eulers(self):
        df = dynamotable.open(self.simple)
        eulers = dynamotable.eulers(df)
        self.assertTrue(eulers.shape[0] == 300)
        self.assertTrue(eulers.shape[1] == 3)

