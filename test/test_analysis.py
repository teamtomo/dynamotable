from unittest import TestCase
from pathlib import Path
import matplotlib.pyplot as plt

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
        self.assertTrue(xyz.shape[1] == 3)

    def test_tilt_sym(self):
        df = dynamotable.open(self.complex)
        df_ts = dynamotable.tilt_sym(df)
        df.plot.scatter('tilt_sym', 'cc', s=0.2)
        ts = df['tilt_sym']
        ts.plot.hist(bins=20)
        plt.show()

    def test_fit_gaussian(self):
        df = dynamotable.open(self.complex)
        df_ts = dynamotable.tilt_sym(df)
        x_fit, y_fit = dynamotable.fit_gaussian(df_ts, 'tilt_sym', 'cc')
        plt.plot(x_fit, y_fit)



