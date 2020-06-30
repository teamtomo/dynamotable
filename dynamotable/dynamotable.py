from pathlib import Path
from typing import Union

import pandas as pd

from .convention import COLUMN_NAMES
from .table_map import table_map_read

def open(table_file: str, table_map_file: str = None) -> pd.DataFrame:
    """
    Opens a dynamo table file, returning a DynamoTable object
    :param table_file:
    :return: dataframe
    """
    # Read into dataframe
    df = pd.read_csv(table_file, header=None, delim_whitespace=True)
    n_cols = df.shape[1]
    if n_cols <= len(COLUMN_NAMES):
        column_names = COLUMN_NAMES[0:n_cols]
        df.columns = column_names

    # In case table has extra columns
    else:
        extra_columns_needed = n_cols - len(COLUMN_NAMES)
        column_names = list(COLUMN_NAMES) + ['' for x in range(extra_columns_needed)]

    # Take absolute value (daxis column sometimes has complex values)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Add table map info
    if table_map_file is not None and Path(table_map_file).exists():
        table_map_dict = table_map_read(table_map_file)
        tomo_file = [table_map_dict[tomo_idx] for tomo_idx in df['tomo']]
        df['tomo_file'] = tomo_file
    return df


def read(filename: str, table_map_file: str = None) -> pd.DataFrame:
    """
    Opens a dynamo table file, returning a pandas DataFrame
    :param filename:
    :return: dataframe
    """
    df = open(filename, table_map_file)
    return df


def new(dataframe: pd.DataFrame, filename: str):
    """
    Writes a dynamo table file from a pandas DataFrame
    :param dataframe: pandas dataframe with headings matching the name from the dynamo table convention
    :param filename: file in which to save data from dataframe, should end in .tbl
    :return:
    """
    # Get n rows
    n_rows = dataframe.shape[0]

    # Check if df has tomo_name but no tomo entry with indices, if so, fix
    if 'tomo_name' in dataframe.columns and 'tomo' not in dataframe.columns:
        tomo_names = dataframe['tomo_name'].unique()
        tomo_name_idx = {name : index for index, name in enumerate(tomo_names)}
        tomo_idx = [tomo_name_idx[name] for name in dataframe['tomo_name']]
        dataframe['tomo'] = tomo_idx

    # Check if tags present in dataframe, if not, make a set of linear tags
    if 'tag' not in dataframe.columns:
        tags = [x+1 for x in range(n_rows)]
        dataframe['tag'] = tags

    # Empty columns will be either 1 or 0, precreate these columns
    zeros = [0 for x in range(n_rows)]
    ones = [1 for x in range(n_rows)]

    # Initialise empty dictionary to store data
    data = {}

    for column_name in COLUMN_NAMES:
        if column_name in dataframe.columns:
            data[column_name] = dataframe[column_name]

        # Aligned value column should set to 1 otherwise alignment projects don't run properly
        elif column_name not in dataframe.columns and column_name == 'aligned_value':
            data[column_name] = ones

        else:
            data[column_name] = zeros

    # Create properly formatted dataframe to write
    table = pd.DataFrame.from_dict(data)

    # Prep filename
    filename = str(filename)
    if not filename.endswith('.tbl'):
        filename = filename.join('.tbl')

    # Write out table
    table.to_csv(filename, sep=' ', header=False, index=False)

    # Write out doc file if appropriate
    if 'tomo_file' in dataframe.columns:
        # Prep table file name
        table_file_name = filename.replace('.tbl', '.doc')

        # Get necessary info in new dataframe
        table_map = dataframe[['tomo', 'tomo_file']]
        table_map.to_csv(table_file_name, sep=' ', header=False, index=False)

    return


def write(dataframe: pd.DataFrame, filename: str):
    """
    Writes a dynamo table file from a pandas DataFrame
    :param dataframe: pandas dataframe with headings matching the name from the dynamo table convention
    :param filename: file in which to save data from dataframe, should end in .tbl
    :return:
    """
    new(dataframe, filename)
    return








