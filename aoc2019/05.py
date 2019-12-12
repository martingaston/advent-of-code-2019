import sys
import unittest
from io import StringIO
from enum import Enum
from utils import read_file_to_list


class Operation(Enum):
    ADDITION = 1
    MULTIPLICATION = 2
    INPUT = 3
    OUTPUT = 4
    HALT = 99


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class Program:
    def __init__(self, program):
        self._program = program

    @classmethod
    def from_intcode(cls, program):
        program_list = [int(x) for x in program]
        return cls(program_list)

    def get(self, index, mode=None):
        if mode is Mode.IMMEDIATE:
            return self._program[index]
        elif mode is Mode.POSITION:
            return self._program[self._program[index]]
        else:
            return self._program[index]

    def set(self, index, value):
        self._program[index] = value

    def __len__(self):
        return len(self._program)


class Instruction:
    def __init__(self, operation, parameter_modes=None):
        self.operation = operation
        self.parameter_modes = parameter_modes

    @classmethod
    def from_int(cls, instruction):
        operation = cls._parse_operation(instruction)
        parameter_modes = cls._parse_parameter_modes(instruction)
        return cls(operation, parameter_modes)

    def parameter(self, index):
        try:
            return self.parameter_modes[index]
        except IndexError:
            return Mode.POSITION

    def _parse_operation(instruction):
        instruction_slice = str(instruction)[-2:]

        return Operation(int(instruction_slice))

    def _parse_parameter_modes(instruction):
        return [Mode(int(i)) for i in str(instruction)[::-1][2:]]


def process_intcode(intcode, intcode_input=sys.stdin, intcode_output=sys.stdout):
    program = Program.from_intcode(intcode)
    pointer = 0

    while pointer < len(program):
        instruction = Instruction.from_int(program.get(pointer))

        if instruction.operation == Operation.HALT:
            break
        elif instruction.operation == Operation.ADDITION:
            augend = program.get(pointer + 1, instruction.parameter(0))
            addend = program.get(pointer + 2, instruction.parameter(1))
            target = program.get(pointer + 3)

            program.set(target, augend + addend)
            pointer += 4
        elif instruction.operation == Operation.MULTIPLICATION:
            multiplier = program.get(pointer + 1, instruction.parameter(0))
            multiplicand = program.get(pointer + 2, instruction.parameter(1))
            target = program.get(pointer + 3)

            program.set(target, multiplier * multiplicand)
            pointer += 4
        elif instruction.operation == Operation.INPUT:
            target = program.get(pointer + 1)
            value = int(intcode_input.readline())
            program.set(target, value)
            pointer += 2
        elif instruction.operation == Operation.OUTPUT:
            output = program.get(pointer + 1, instruction.parameter(0))

            intcode_output.write(str(output))
            pointer += 2
        else:
            raise ValueError("opcode should be 1, 2 or 99")

    return program._program


if __name__ == "__main__":
    test_diagnostic_program = [
        int(x) for x in read_file_to_list("input/05.txt")[0].split(",")
    ]
    process_intcode(test_diagnostic_program)


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

    def test_instruction_works_with_negative_numbers(self):
        result = process_intcode([1101, 100, -1, 4, 99])

        self.assertEqual([1101, 100, -1, 4, 99], result)
