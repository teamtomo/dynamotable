from .constants import COLUMN_NAME_TO_COLUMN_NUMBER

COLUMN_NUMBER_TO_COLUMN_NAME = {value: key for key, value in COLUMN_NAME_TO_COLUMN_NUMBER.items()}
COLUMN_NAMES = tuple(COLUMN_NAME_TO_COLUMN_NUMBER.keys())


def column_name_to_column_number(column_name):
    return COLUMN_NAME_TO_COLUMN_NUMBER[column_name]


def column_number_to_column_name(column_number):
    return COLUMN_NUMBER_TO_COLUMN_NAME[column_number]


def generate_column_names(n_cols):
    """generate a list of column names according to the Dynamo convention.
    """
    if n_cols <= len(COLUMN_NAMES):
        column_names = COLUMN_NAMES[0:n_cols]
    else:
        extra_columns_needed = n_cols - len(COLUMN_NAMES)
        column_names = list(COLUMN_NAMES) + ['' for x in range(extra_columns_needed)]
    return column_names


def sanitise_table_filename(filename):
    filename = str(filename)
    if not filename.endswith('.tbl'):
        filename = filename + '.tbl'
    return filename


def write_table_map(df, filename):
    table_map = df[['tomo', 'tomo_file']].drop_duplicates(subset='tomo')
    table_map.to_csv(filename, sep=' ', header=False, index=False)
