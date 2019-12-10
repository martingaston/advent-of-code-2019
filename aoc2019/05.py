import sys
import unittest
from io import StringIO

class Opcode:
    def __init__(self, instruction):
        self.instruction = instruction

    @classmethod
    def from_int(cls, opcode):
        instruction = cls._parse_instruction(opcode)
        return cls(instruction)

    def _parse_instruction(instruction):
        return {
            1: "ADDITION",
            2: "MULTIPLICATION",
            3: "INPUT",
            4: "OUTPUT",
            99: "HALT",
        }.get(instruction)


def process_intcode(intcode, intcode_input=sys.stdin, intcode_output=sys.stdout):
    intcode = intcode.copy()  # shadow intcode to stop mutation outside of the block
    pointer = 0

    while pointer < len(intcode):
        opcode = {
            1: "ADDITION",
            2: "MULTIPLICATION",
            3: "INPUT",
            4: "OUTPUT",
            99: "HALT",
        }.get(intcode[pointer])

        if opcode == "HALT":
            break
        elif opcode == "ADDITION":
            augend = intcode[pointer + 1]
            addend = intcode[pointer + 2]
            target = intcode[pointer + 3]

            intcode[target] = intcode[augend] + intcode[addend]
            pointer += 4
        elif opcode == "MULTIPLICATION":
            multiplier = intcode[pointer + 1]
            multiplicand = intcode[pointer + 2]
            target = intcode[pointer + 3]

            intcode[target] = intcode[multiplier] * intcode[multiplicand]
            pointer += 4
        elif opcode == "INPUT":
            target = intcode[pointer + 1]
            value = int(intcode_input.readline())
            intcode[target] = value
            pointer += 2
        elif opcode == "OUTPUT":
            output = intcode[intcode[pointer + 1]]
            intcode_output.write(str(output))
            pointer += 2
        else:
            raise ValueError("opcode should be 1, 2 or 99")

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

    def test_opcode_three_inputs_value(self):
        intcode_input = StringIO("66\n")

        result = process_intcode([3, 0, 99], intcode_input=intcode_input)

        self.assertEqual([66, 0, 99], result)

    def test_opcode_four_outputs_value(self):
        intcode_output = StringIO()

        result = process_intcode([4, 0], intcode_output=intcode_output)

        self.assertEqual(intcode_output.getvalue().strip(), "4")

    def test_input_and_output_together(self):
        intcode_input = StringIO("66\n")
        intcode_output = StringIO()

        result = process_intcode(
            [3, 0, 4, 0, 99],
            intcode_input=intcode_input,
            intcode_output=intcode_output,
        )

        self.assertEqual([66, 0, 4, 0, 99], result)
        self.assertEqual("66", intcode_output.getvalue().strip())

    def test_intcode_can_read_multiple_commands(self):
        result = process_intcode([1, 0, 0, 0, 1, 0, 0, 0, 99])

        self.assertEqual([4, 0, 0, 0, 1, 0, 0, 0, 99], result)

    def test_intcode_can_be_edited_during_iteration(self):
        result = process_intcode([1, 1, 1, 4, 99, 5, 6, 0, 99])

        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], result)

    def test_opcode_class_can_set_instruction(self):
        opcode_addition = Opcode.from_int(1)
        opcode_multiplication = Opcode.from_int(2)

        self.assertEqual("ADDITION", opcode_addition.instruction)
        self.assertEqual("MULTIPLICATION", opcode_multiplication.instruction)
