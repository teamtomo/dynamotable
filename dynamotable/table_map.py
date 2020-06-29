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
