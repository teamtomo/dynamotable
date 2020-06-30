import pandas as pd
import numpy as np
from scipy.optimize import curve_fit


def xyz(dataframe: pd.DataFrame) -> np.ndarray:
    xyz_orig = dataframe[['x', 'y', 'z']].to_numpy()
    dxyz = dataframe[['dx', 'dy', 'dz']].to_numpy()
    xyz = xyz_orig + dxyz
    return xyz


def eulers(dataframe: pd.DataFrame) -> np.ndarray:
    eulers = dataframe[['tdrot', 'tilt', 'narot']].to_numpy()
    return eulers


def split(dataframe: pd.DataFrame) -> dict:
    unique_tomo_idx = dataframe['tomo'].unique()
    df_split = {}

    for idx in unique_tomo_idx:
        df_split[idx] = dataframe[dataframe['tomo'] == idx]
    return df_split


def tilt_sym(dataframe: pd.DataFrame) -> pd.DataFrame:
    tilt = dataframe['tilt'].copy().to_numpy()
    idx = tilt > 90
    tilt[idx] = tilt[idx] - 90
    dataframe['tilt_sym'] = tilt
    return dataframe

def fit_gaussian(dataframe: pd.DataFrame, x_col, y_col) -> pd.DataFrame:
    def gauss(x, *p):
        A, mu, sigma = p
        return A * np.exp(-(x-mu)**2 / (2.*sigma**2))
    mu0 = dataframe[x_col].mean
    p0 = [0.1, mu0, 45]

    coeff, var_matrix = curve_fit(gauss, dataframe[x_col], dataframe[y_col], p0=p0)
    xmin = dataframe[x_col].min()
    xmax = dataframe[x_col].max()
    linspace_x = np.linspace(xmin, xmax, 1000)
    return linspace_x, gauss(linspace_x, *coeff)