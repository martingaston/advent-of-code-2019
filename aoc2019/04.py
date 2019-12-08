import unittest
import itertools

INPUT = range(145852, 616943)  # need to +1 from AoC input as Python range is exclusive


class Password:
    @staticmethod
    def is_valid_part_one(password):
        return (
            Password._has_six_digits(password)
            and Password._has_at_least_two_adjacent_digits(password)
            and Password._digits_do_not_decrease(password)
        )

    @staticmethod
    def is_valid_part_two(password):
        return (
            Password._has_six_digits(password)
            and Password._has_only_two_adjacent_digits(password)
            and Password._digits_do_not_decrease(password)
        )

    @staticmethod
    def count_valid_part_one(passwords):
        return sum(Password._validate_iter(passwords, Password.is_valid_part_one))

    @staticmethod
    def count_valid_part_two(passwords):
        return sum(Password._validate_iter(passwords, Password.is_valid_part_two))

    def _validate_iter(passwords, validator):
        for password in passwords:
            yield validator(password)

    def _has_six_digits(password):
        return len(str(password)) == 6

    def _has_at_least_two_adjacent_digits(password):
        password_digits = map(lambda x: int(x), str(password))
        for _, consequtive_digits in itertools.groupby(password_digits):
            if len(list(consequtive_digits)) > 1:
                return True

        return False

    def _has_only_two_adjacent_digits(password):
        password_digits = map(lambda x: int(x), str(password))
        for _, consequtive_digits in itertools.groupby(password_digits):
            if len(list(consequtive_digits)) == 2:
                return True

        return False

    def _digits_do_not_decrease(password):
        password_digits = list(map(lambda x: int(x), str(password)))
        for index, digit in enumerate(password_digits):
            if index == 0:
                continue

            if digit < password_digits[index - 1]:
                return False

        return True


if __name__ == "__main__":
    print("DAY 4")
    print(
        f"Part 1: There are {Password.count_valid_part_one(INPUT)} valid passwords in the input"
    )
    print(
        f"Part 2: There are {Password.count_valid_part_two(INPUT)} valid passwords in the input"
    )


class Test(unittest.TestCase):
    def test_is_working(self):
        self.assertEqual(15 % 5, 0)

    def test_password_contains_six_digits(self):
        self.assertFalse(Password.is_valid_part_one(12345))
        self.assertTrue(Password.is_valid_part_one(111111))
        self.assertFalse(Password.is_valid_part_one(1234567))

    def test_password_has_two_adjacent_digits(self):
        self.assertFalse(Password.is_valid_part_one(123456))
        self.assertTrue(Password.is_valid_part_one(122345))

    def test_digits_do_not_decrease(self):
        self.assertFalse(Password.is_valid_part_one(223450))
        self.assertTrue(Password.is_valid_part_one(123455))

    def test_111111_is_a_valid_password(self):
        password = 111111

        self.assertTrue(Password.is_valid_part_one(password))

    def test_123789_is_not_a_valid_password(self):
        password = 123789  # no double

        self.assertFalse(Password.is_valid_part_one(password))

    def test_223450_is_not_a_valid_password(self):
        password = 223450  # decreases

        self.assertFalse(Password.is_valid_part_one(password))

    def test_count_valid_passwords(self):
        passwords = [111111, 111112, 111113, 654321]

        self.assertEqual(3, Password.count_valid_part_one(passwords))

    def test_count_valid_password_range(self):
        passwords = range(111111, 111115)

        self.assertEqual(4, Password.count_valid_part_one(passwords))

    def test_112233_is_valid_for_part_two(self):
        self.assertTrue(Password.is_valid_part_two(112233))

    def test_123444_is_not_valid_for_part_two(self):
        self.assertFalse(Password.is_valid_part_two(123444))

    def test_111122_is_valid_for_part_two(self):
        self.assertTrue(Password.is_valid_part_two(111122))
