def read_file_to_list(path):
    with open(path) as fp:
        return [line.rstrip() for line in fp]
