import unittest
from utils import read_file_to_list

def process_intcode(intcode):
    cursor = 0

    while cursor < len(intcode):
        opcode = intcode[cursor]

        if opcode == 99:
            break
        elif opcode == 1:
            augend = intcode[cursor + 1]
            addend = intcode[cursor + 2]
            target = intcode[cursor + 3]

            intcode[target] = intcode[augend] + intcode[addend]
        elif opcode == 2:
            multiplier = intcode[cursor + 1]
            multiplicand = intcode[cursor + 2]
            target = intcode[cursor + 3]

            intcode[target] = intcode[multiplier] * intcode[multiplicand]
        else:
            raise ValueError("opcode should be 1, 2 or 99")
        cursor += 4

    return intcode

if __name__ == '__main__':
    intcode = [int(x) for x in read_file_to_list("input/02.txt")[0].split(",")]

    # replace two positions with hardcoded data (via instructions)
    intcode[1] = 12
    intcode[2] = 2

    print(process_intcode(intcode))
    print(f"the value at position 0 after the program halts is: {intcode[0]}")

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

    def test_intcode_can_read_multiple_commands(self):
        result = process_intcode([1, 0, 0, 0, 1, 0, 0, 0, 99])

        self.assertEqual([4, 0, 0, 0, 1, 0, 0, 0, 99], result)

    def test_intcode_can_be_edited_during_iteration(self):
        result = process_intcode([1, 1, 1, 4, 99, 5, 6, 0, 99])

        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], result)
