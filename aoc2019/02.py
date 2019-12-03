import unittest
from utils import read_file_to_list

def process_intcode(intcode):
    cursor = 0
    opcode = intcode[cursor]

    if opcode == 99:
        return intcode
    elif opcode == 1:
        augend = intcode[cursor + 1]
        addend = intcode[cursor + 2]
        target = intcode[cursor + 3]

        intcode[target] = intcode[augend] + intcode[addend]
        return intcode
    elif opcode == 2:
        multiplier = intcode[cursor + 1]
        multiplicand = intcode[cursor + 2]
        target = intcode[cursor + 3]

        intcode[target] = intcode[multiplier] * intcode[multiplicand]
        return intcode
    else:
        raise ValueError("opcode should be 1, 2 or 99")

if __name__ == '__main__':
    intcode = [int(x) for x in read_file_to_list("input/02.txt")[0].split(",")]
    print(intcode)

class Test(unittest.TestCase):
    def test_setup_properly(self):
        self.assertEqual(10, 5 + 5)

    def test_opcode_of_99_halts(self):
        result = process_intcode([99])

        self.assertEqual([99], result)

    def test_opcode_one_handles_addition(self):
        result = process_intcode([1, 0, 0, 0, 99])

        self.assertEqual([2, 0, 0, 0, 99], result)

    def test_opcode_two_handles_multiplication(self):
        result = process_intcode([2, 3, 0, 3, 99])

        self.assertEqual([2, 3, 0, 6, 99], result)
