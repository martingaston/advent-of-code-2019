import sys
import unittest
from io import StringIO
from enum import Enum
from utils import read_file_to_list


class Pointer:
    def __init__(self):
        self._position = 0

    def get(self):
        return self._position

    def jump(self, position):
        self._position = int(position)


class Operation(Enum):
    ADDITION = 1
    MULTIPLICATION = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99

    @staticmethod
    def addition(program, instruction, pointer):
        current_pointer = pointer.get()
        augend = program.get(current_pointer + 1, instruction.parameter(0))
        addend = program.get(current_pointer + 2, instruction.parameter(1))
        target = program.get(current_pointer + 3)

        program.set(target, augend + addend)
        pointer.jump(current_pointer + 4)

    @staticmethod
    def multiplication(program, instruction, pointer):
        current_pointer = pointer.get()
        multiplier = program.get(current_pointer + 1, instruction.parameter(0))
        multiplicand = program.get(current_pointer + 2, instruction.parameter(1))
        target = program.get(current_pointer + 3)

        program.set(target, multiplier * multiplicand)
        pointer.jump(current_pointer + 4)

    @staticmethod
    def input(program, instruction, pointer, intcode_input):
        current_pointer = pointer.get()
        target = program.get(current_pointer + 1)
        value = int(intcode_input.readline())

        program.set(target, value)
        pointer.jump(current_pointer + 2)

    @staticmethod
    def output(program, instruction, pointer, intcode_output):
        current_pointer = pointer.get()
        output = program.get(current_pointer + 1, instruction.parameter(0))

        intcode_output.write(str(output))
        pointer.jump(current_pointer + 2)

    @staticmethod
    def jump_if_true(program, instruction, pointer):
        current_pointer = pointer.get()
        predicate = program.get(current_pointer + 1, instruction.parameter(0)) is not 0

        pointer.jump(
            program.get(current_pointer + 2, instruction.parameter(1))
            if predicate
            else current_pointer + 3
        )

    @staticmethod
    def jump_if_false(program, instruction, pointer):
        current_pointer = pointer.get()
        predicate = program.get(current_pointer + 1, instruction.parameter(0)) is 0

        pointer.jump(
            program.get(current_pointer + 2, instruction.parameter(1))
            if predicate
            else current_pointer + 3
        )

    @staticmethod
    def less_than(program, instruction, pointer):
        current_pointer = pointer.get()
        predicate = program.get(
            current_pointer + 1, instruction.parameter(0)
        ) < program.get(current_pointer + 2, instruction.parameter(1))
        target = program.get(current_pointer + 3)

        program.set(target, 1 if predicate else 0)
        pointer.jump(current_pointer + 4)

    @staticmethod
    def equals(program, instruction, pointer):
        current_pointer = pointer.get()
        predicate = program.get(
            current_pointer + 1, instruction.parameter(0)
        ) is program.get(current_pointer + 2, instruction.parameter(1))

        target = program.get(current_pointer + 3)

        program.set(target, 1 if predicate else 0)
        pointer.jump(current_pointer + 4)


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
    pointer = Pointer()

    while pointer.get() < len(program):
        instruction = Instruction.from_int(program.get(pointer.get()))

        if instruction.operation == Operation.HALT:
            break
        elif instruction.operation == Operation.ADDITION:
            Operation.addition(program, instruction, pointer)
        elif instruction.operation == Operation.MULTIPLICATION:
            Operation.multiplication(program, instruction, pointer)
        elif instruction.operation == Operation.INPUT:
            Operation.input(program, instruction, pointer, intcode_input)
        elif instruction.operation == Operation.OUTPUT:
            Operation.output(program, instruction, pointer, intcode_output)
        elif instruction.operation == Operation.JUMP_IF_TRUE:
            Operation.jump_if_true(program, instruction, pointer)
        elif instruction.operation == Operation.JUMP_IF_FALSE:
            Operation.jump_if_false(program, instruction, pointer)
        elif instruction.operation == Operation.LESS_THAN:
            Operation.less_than(program, instruction, pointer)
        elif instruction.operation == Operation.EQUALS:
            Operation.equals(program, instruction, pointer)
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

    def test_output_is_one_if_input_is_equal_to_eight(self):
        intcode_input = StringIO("8\n")
        intcode_output = StringIO()

        result = process_intcode(
            [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], intcode_input, intcode_output
        )

        self.assertEqual(intcode_output.getvalue().strip(), "1")

    def test_output_is_zero_if_input_not_less_than_eight(self):
        intcode_input = StringIO("15\n")
        intcode_output = StringIO()

        result = process_intcode(
            [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], intcode_input, intcode_output
        )

        self.assertEqual(intcode_output.getvalue().strip(), "0")

    def test_output_is_zero_if_input_is_equal_to_eight_in_immediate_mode(self):
        intcode_input = StringIO("999\n")
        intcode_output = StringIO()

        result = process_intcode(
            [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], intcode_input, intcode_output
        )

        self.assertEqual(intcode_output.getvalue().strip(), "0")

    def test_output_is_zero_if_input_not_less_than_eight_in_immediate_mode(self):
        intcode_input = StringIO("5\n")
        intcode_output = StringIO()

        result = process_intcode(
            [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], intcode_input, intcode_output
        )

        self.assertEqual(intcode_output.getvalue().strip(), "1")

    def test_input_is_non_zero(self):
        intcode_input = StringIO("5\n")
        intcode_output = StringIO()

        result = process_intcode(
            [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
            intcode_input,
            intcode_output,
        )

        self.assertEqual(intcode_output.getvalue().strip(), "1")

    def test_input_is_non_zero_in_immediate_mode(self):
        intcode_input = StringIO("0\n")
        intcode_output = StringIO()

        result = process_intcode(
            [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
            intcode_input,
            intcode_output,
        )

        self.assertEqual(intcode_output.getvalue().strip(), "0")
