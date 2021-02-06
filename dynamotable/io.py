from pathlib import Path

import pandas as pd

from .convention import COLUMN_NAMES


def read(table_file: str, table_map_file: str = None) -> pd.DataFrame:
    """
    read a dynamo table file into a pandas dataframe
    """
    # Read into dataframe
    df = pd.read_csv(table_file, header=None, delim_whitespace=True)

    # Get column names
    n_cols = df.shape[1]
    if n_cols <= len(COLUMN_NAMES):
        column_names = COLUMN_NAMES[0:n_cols]
    else:
        extra_columns_needed = n_cols - len(COLUMN_NAMES)
        column_names = list(COLUMN_NAMES) + ['' for x in range(extra_columns_needed)]

    # Take absolute value (daxis column sometimes has complex values)
    df = df.apply(pd.to_numeric, errors='ignore')
    df.columns = column_names

    # Add table map info into dataframe
    if table_map_file is not None and Path(table_map_file).exists():
        table_map_dict = table_map_read(table_map_file)
        tomo_file = [table_map_dict[tomo_idx] for tomo_idx in df['tomo']]
        df['tomo_file'] = tomo_file
    return df


def write(dataframe: pd.DataFrame, filename: str):
    """
    Writes a dynamo table file from a pandas DataFrame
    """
    # Get n rows
    n_rows = dataframe.shape[0]

    # Check if df has tomo_name but no tomo entry with indices, if so, fix
    if 'tomo_file' in dataframe.columns and 'tomo' not in dataframe.columns:
        tomo_names = dataframe['tomo_file'].unique()
        tomo_name_idx = {name: index for index, name in enumerate(tomo_names)}
        tomo_idx = [tomo_name_idx[name] for name in dataframe['tomo_file']]
        dataframe['tomo'] = tomo_idx

    # Check if tags present in dataframe, if not, make a set of linear tags
    if 'tag' not in dataframe.columns:
        tags = [x + 1 for x in range(n_rows)]
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

    # Write out tomogram-table map file if appropriate
    if 'tomo_file' in dataframe.columns:
        table_map_file_name = filename.replace('.tbl', '.doc')

        # Get necessary info in new dataframe
        table_map = dataframe[['tomo', 'tomo_file']].drop_duplicates(subset='tomo')
        table_map.to_csv(table_map_file_name, sep=' ', header=False, index=False)

    return


def table_map_read(filename: str) -> dict:
    """
    Reads dynamo table map file
    :param file: table map file from dynamo
    :return: dict of form {idx : '/path/to/tomogram'}
    """
    table_map = open(filename, 'r')
    lines = table_map.readlines()

    out_dict = {}
    for line in lines:
        idx, path = line.strip().split()
        out_dict[int(idx)] = path

    table_map.close()
    return out_dict
