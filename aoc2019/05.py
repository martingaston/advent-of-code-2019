import sys
import unittest
from io import StringIO
from enum import Enum


class Operation(Enum):
    ADDITION = 1
    MULTIPLICATION = 2
    INPUT = 3
    OUTPUT = 4
    HALT = 99


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class Instruction:
    def __init__(self, operation, parameter_modes=None):
        self.operation = operation
        self.parameter_modes = parameter_modes

    @classmethod
    def from_int(cls, instruction):
        operation = cls._parse_operation(instruction)
        parameter_modes = cls._parse_parameter_modes(instruction)
        return cls(operation, parameter_modes)

    def _parse_operation(instruction):
        instruction_slice = str(instruction)[-2:]

        return Operation(int(instruction_slice))

    def _parse_parameter_modes(instruction):
        return [Mode(int(i)) for i in str(instruction)[::-1][2:]]


def process_intcode(intcode, intcode_input=sys.stdin, intcode_output=sys.stdout):
    intcode = intcode.copy()  # shadow intcode to stop mutation outside of the block
    pointer = 0

    while pointer < len(intcode):
        instruction = Instruction.from_int(intcode[pointer])

        if instruction.operation == Operation.HALT:
            break
        elif instruction.operation == Operation.ADDITION:
            augend = intcode[pointer + 1]
            addend = intcode[pointer + 2]
            target = intcode[pointer + 3]

            intcode[target] = intcode[augend] + intcode[addend]
            pointer += 4
        elif instruction.operation == Operation.MULTIPLICATION:
            if (
                len(instruction.parameter_modes) < 1
                or instruction.parameter_modes[0] is Mode.POSITION
            ):
                multiplier = intcode[intcode[pointer + 1]]
            elif instruction.parameter_modes[0] is Mode.IMMEDIATE:
                multiplier = intcode[pointer + 1]

            if (
                len(instruction.parameter_modes) < 2
                or instruction.parameter_modes[1] is Mode.POSITION
            ):
                multiplicand = intcode[intcode[pointer + 2]]
            elif instruction.parameter_modes[1] is Mode.IMMEDIATE:
                multiplicand = intcode[pointer + 2]

            target = intcode[pointer + 3]

            intcode[target] = multiplier * multiplicand
            pointer += 4
        elif instruction.operation == Operation.INPUT:
            target = intcode[pointer + 1]
            value = int(intcode_input.readline())
            intcode[target] = value
            pointer += 2
        elif instruction.operation == Operation.OUTPUT:
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

    def test_instruction_class_can_set_instruction(self):
        instruction_addition = Instruction.from_int(1)
        instruction_multiplication = Instruction.from_int(2)

        self.assertEqual(Operation.ADDITION, instruction_addition.operation)
        self.assertEqual(Operation.MULTIPLICATION, instruction_multiplication.operation)

    def test_opcode_class_can_parse_parameter_mode(self):
        instruction = Instruction.from_int(1002)

        self.assertEqual(instruction.parameter_modes, [Mode.POSITION, Mode.IMMEDIATE])
        self.assertEqual(instruction.operation, Operation.MULTIPLICATION)

    def test_opcode_parameter_that_writes_will_not_be_in_immediate_mode(self):
        pass

    def test_instruction_can_process_immediate_mode(self):
        result = process_intcode([1002, 4, 3, 4, 33])

        self.assertEqual([1002, 4, 3, 4, 99], result)
