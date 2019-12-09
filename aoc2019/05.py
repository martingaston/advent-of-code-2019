import unittest


def process_intcode(intcode):
    intcode = intcode.copy()  # shadow intcode to stop mutation outside of the block
    pointer = 0

    while pointer < len(intcode):
        opcode = {1: "ADDITION", 2: "MULTIPLICATION", 99: "HALT",}.get(intcode[pointer])

        if opcode == "HALT":
            break
        elif opcode == "ADDITION":
            augend = intcode[pointer + 1]
            addend = intcode[pointer + 2]
            target = intcode[pointer + 3]

            intcode[target] = intcode[augend] + intcode[addend]
        elif opcode == "MULTIPLICATION":
            multiplier = intcode[pointer + 1]
            multiplicand = intcode[pointer + 2]
            target = intcode[pointer + 3]

            intcode[target] = intcode[multiplier] * intcode[multiplicand]
        else:
            raise ValueError("opcode should be 1, 2 or 99")
        pointer += 4

    return intcode


if __name__ == "__main__":
    pass


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
