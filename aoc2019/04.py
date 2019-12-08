import unittest
import itertools

INPUT = range(145852, 616943)  # need to +1 from AoC input as Python range is exclusive


class Password:
    @staticmethod
    def is_valid(password):
        return (
            Password._has_six_digits(password)
            and Password._has_two_adjacent_digits(password)
            and Password._digits_do_not_decrease(password)
        )

    @staticmethod
    def count_valid(passwords):
        return sum(Password._validate_iter(passwords))

    def _validate_iter(passwords):
        for password in passwords:
            yield Password.is_valid(password)

    def _has_six_digits(password):
        return len(str(password)) == 6

    def _has_two_adjacent_digits(password):
        password_digits = map(lambda x: int(x), str(password))
        for _, consequtive_digits in itertools.groupby(password_digits):
            if len(list(consequtive_digits)) > 1:
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
        f"Part 1: There are {Password.count_valid(INPUT)} valid passwords in the input"
    )


class Test(unittest.TestCase):
    def test_is_working(self):
        self.assertEqual(15 % 5, 0)

    def test_password_contains_six_digits(self):
        self.assertFalse(Password.is_valid(12345))
        self.assertTrue(Password.is_valid(111111))
        self.assertFalse(Password.is_valid(1234567))

    def test_password_has_two_adjacent_digits(self):
        self.assertFalse(Password.is_valid(123456))
        self.assertTrue(Password.is_valid(122345))

    def test_digits_do_not_decrease(self):
        self.assertFalse(Password.is_valid(223450))
        self.assertTrue(Password.is_valid(123455))

    def test_111111_is_a_valid_password(self):
        password = 111111

        self.assertTrue(Password.is_valid(password))

    def test_123789_is_not_a_valid_password(self):
        password = 123789  # no double

        self.assertFalse(Password.is_valid(password))

    def test_223450_is_not_a_valid_password(self):
        password = 223450  # decreases

        self.assertFalse(Password.is_valid(password))

    def test_count_valid_passwords(self):
        passwords = [111111, 111112, 111113, 654321]

        self.assertEqual(3, Password.count_valid(passwords))

    def test_count_valid_password_range(self):
        passwords = range(111111, 111115)

        self.assertEqual(4, Password.count_valid(passwords))
