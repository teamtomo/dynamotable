"""Helpers for Dynamo table column names and file names."""

from pathlib import Path

import pandas as pd

from .constants import COLUMN_NAME_TO_COLUMN_NUMBER

COLUMN_NUMBER_TO_COLUMN_NAME = {
    value: key for key, value in COLUMN_NAME_TO_COLUMN_NUMBER.items()
}
COLUMN_NAMES = tuple(COLUMN_NAME_TO_COLUMN_NUMBER.keys())


def column_name_to_column_number(column_name: str) -> int:
    """Return the 1-indexed Dynamo column number for a column name."""
    return COLUMN_NAME_TO_COLUMN_NUMBER[column_name]


def column_number_to_column_name(column_number: int) -> str:
    """Return the column name for a 1-indexed Dynamo column number."""
    return COLUMN_NUMBER_TO_COLUMN_NAME[column_number]


def generate_column_names(n_cols: int) -> list[str]:
    """Generate a list of column names according to the Dynamo convention."""
    column_names: list[str]
    if n_cols <= len(COLUMN_NAMES):
        column_names = list(COLUMN_NAMES[0:n_cols])
    else:
        extra_columns_needed = n_cols - len(COLUMN_NAMES)
        column_names = list(COLUMN_NAMES) + ["" for x in range(extra_columns_needed)]
    return column_names


def sanitise_table_filename(filename: str | Path) -> str:
    """Return the filename as a string with a .tbl extension."""
    filename = str(filename)
    if not filename.endswith(".tbl"):
        filename = filename + ".tbl"
    return filename


def write_table_map(df: pd.DataFrame, filename: str) -> None:
    """Write the tomogram index to file name map for a table."""
    table_map = df[["tomo", "tomo_file"]].drop_duplicates(subset="tomo")
    table_map.to_csv(filename, sep=" ", header=False, index=False)
