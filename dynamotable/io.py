from pathlib import Path

import pandas as pd

from .utils import COLUMN_NAMES, generate_column_names, sanitise_table_filename, write_table_map


def read(table_file: str, table_map_file: str = None) -> pd.DataFrame:
    """
    read a dynamo table file into a pandas dataframe
    """
    # Read into dataframe
    df = pd.read_csv(table_file, header=None, delim_whitespace=True)

    # Get column names
    n_cols = df.shape[1]
    column_names = generate_column_names(n_cols)

    # Take absolute value (daxis column sometimes has complex values)
    df = df.apply(pd.to_numeric, errors='ignore')
    df.columns = column_names

    # Add table map info into dataframe
    if table_map_file is not None and Path(table_map_file).exists():
        table_map = read_table_map(table_map_file)
        df = df.merge(table_map)
    return df


def write(df: pd.DataFrame, filename: str):
    """
    Writes a dynamo table file from a pandas DataFrame
    """
    # Get n rows
    n_rows = df.shape[0]

    # Check if df has tomo_name but no tomo entry with indices, if so, fix
    if 'tomo_file' in df.columns and 'tomo' not in df.columns:
        tomo_names = df['tomo_file'].unique()
        tomo_name_idx = {name: index for index, name in enumerate(tomo_names)}
        tomo_idx = [tomo_name_idx[name] for name in df['tomo_file']]
        df['tomo'] = tomo_idx

    # Initialise empty dictionary to store data before writing and generate some
    # data for empty columns
    data = {}
    zeros = [0 for x in range(n_rows)]
    ones = [1 for x in range(n_rows)]
    tags = [x + 1 for x in range(n_rows)]

    for column_name in COLUMN_NAMES:
        if column_name in df.columns:
            data[column_name] = df[column_name]
        elif column_name == 'tag':
            data[column_name] = tags
        elif column_name == 'aligned_value':
            data[column_name] = ones
        else:
            data[column_name] = zeros
    table = pd.DataFrame.from_dict(data)

    # Write out table
    filename = sanitise_table_filename(filename)
    table.to_csv(filename, sep=' ', header=False, index=False)

    # Write out tomogram-table map file if appropriate
    if 'tomo_file' in df.columns:
        write_table_map(df, filename.replace('.tbl', '.doc'))
    return


def read_table_map(table_map_file: str) -> dict:
    """Read a Dynamo table map file into a dataframe
    """
    table_map = pd.read_csv(table_map_file, header=None, delim_whitespace=True)
    table_map.columns = ['tomo', 'tomo_file']
    return table_map
