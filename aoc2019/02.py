import unittest
from utils import read_file_to_list

if __name__ == '__main__':
    intcode = read_file_to_list("input/02.txt")[0].split(",")
    print(intcode)
