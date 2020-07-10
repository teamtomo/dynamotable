import pandas as pd
import numpy as np

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
