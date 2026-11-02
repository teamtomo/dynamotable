"""Reading and writing Dynamo table files."""

from pathlib import Path
from typing import Any

import pandas as pd

from .utils import (
    COLUMN_NAMES,
    generate_column_names,
    sanitise_table_filename,
    write_table_map,
)


def _safe_to_numeric(col: pd.Series) -> pd.Series:
    """Convert column to numeric, returning original if conversion fails."""
    try:
        return pd.to_numeric(col)
    except (ValueError, TypeError):
        return col


def read(table_file: str, table_map_file: str | None = None) -> pd.DataFrame:
    """Read a Dynamo table file into a pandas DataFrame.

    Parameters
    ----------
    table_file : str
        Path to the Dynamo table (``.tbl``) file.
    table_map_file : str or None, optional
        Path to a table map (``.doc``) file that maps tomogram indices to
        tomogram files. If given and the file exists, its ``tomo_file``
        column is merged into the result on the ``tomo`` column.

    Returns
    -------
    pandas.DataFrame
        One row per particle, with columns named after the Dynamo table
        convention.
    """
    # Read into dataframe
    df = pd.read_csv(table_file, header=None, sep=r"\s+")

    # Get column names
    n_cols = df.shape[1]
    column_names = generate_column_names(n_cols)

    # Take absolute value (daxis column sometimes has complex values)
    df = df.apply(_safe_to_numeric)
    df.columns = pd.Index(column_names)

    # Add table map info into dataframe
    if table_map_file is not None and Path(table_map_file).exists():
        table_map = read_table_map(table_map_file)
        df = df.merge(table_map)
    return df


def write(df: pd.DataFrame, filename: str) -> None:
    """Write a Dynamo table file from a pandas DataFrame.

    Columns missing from ``df`` are filled with defaults: ``tag`` counts from
    1, ``aligned_value`` is 1 and everything else is 0. If ``df`` has a
    ``tomo_file`` column, a table map (``.doc``) file is written next to the
    table, and a ``tomo`` index column is added to ``df`` if it has none.

    Parameters
    ----------
    df : pandas.DataFrame
        Particle data, with columns named after the Dynamo table convention.
    filename : str
        Path of the table to write. ``.tbl`` is appended if missing.
    """
    # Get n rows
    n_rows = df.shape[0]

    # Check if df has tomo_name but no tomo entry with indices, if so, fix
    if "tomo_file" in df.columns and "tomo" not in df.columns:
        tomo_names = df["tomo_file"].unique()
        tomo_name_idx = {name: index for index, name in enumerate(tomo_names)}
        tomo_idx = [tomo_name_idx[name] for name in df["tomo_file"]]
        df["tomo"] = tomo_idx

    # Initialise empty dictionary to store data before writing and generate some
    # data for empty columns
    data: dict[str, Any] = {}
    zeros = [0 for x in range(n_rows)]
    ones = [1 for x in range(n_rows)]
    tags = [x + 1 for x in range(n_rows)]

    for column_name in COLUMN_NAMES:
        if column_name in df.columns:
            data[column_name] = df[column_name]
        elif column_name == "tag":
            data[column_name] = tags
        elif column_name == "aligned_value":
            data[column_name] = ones
        else:
            data[column_name] = zeros
    table = pd.DataFrame.from_dict(data)

    # Write out table
    filename = sanitise_table_filename(filename)
    table.to_csv(filename, sep=" ", header=False, index=False)

    # Write out tomogram-table map file if appropriate
    if "tomo_file" in df.columns:
        write_table_map(df, filename.replace(".tbl", ".doc"))


def read_table_map(table_map_file: str) -> pd.DataFrame:
    """Read a Dynamo table map file into a dataframe."""
    return pd.read_csv(
        table_map_file, header=None, sep=r"\s+", names=["tomo", "tomo_file"]
    )
