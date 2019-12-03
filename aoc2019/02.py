import unittest
from utils import read_file_to_list

def process_intcode(intcode):
    return [99]

if __name__ == '__main__':
    intcode = read_file_to_list("input/02.txt")[0].split(",")
    print(intcode)

class Test(unittest.TestCase):
    def test_setup_properly(self):
        self.assertEqual(10, 5 + 5)

    def test_opcode_of_99_halts(self):
        result = process_intcode([99])

        self.assertEqual([99], result)
