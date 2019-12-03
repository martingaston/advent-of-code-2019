import unittest
from functools import reduce
from utils import read_file_to_list

def fuel_from_mass(mass):
    return int(mass) // 3 - 2

def sum_list_of_mass_modules(mass_list):
    return reduce(lambda total, current: total + fuel_from_mass(current), mass_list, 0)

def total_fuel_from_mass(mass):
    fuel = fuel_from_mass(mass)

    if fuel <= 0:
        return 0
    else:
        return fuel + total_fuel_from_mass(fuel)

def sum_updated_list_of_mass_modules(mass_list):
    return reduce(lambda total, current: total + total_fuel_from_mass(current), mass_list, 0)

if __name__ == '__main__':
    mass_modules = read_file_to_list("input/01.txt")
    print(sum_list_of_mass_modules(mass_modules))
    print(sum_updated_list_of_mass_modules(mass_modules))


class Test(unittest.TestCase):
    def test_setup_properly(self):
        self.assertEqual(2, 1+1)

    def test_mass_of_twelve_equals_fuel_of_two(self):
        fuel = fuel_from_mass(12)

        self.assertEqual(fuel, 2)

    def test_mass_of_ninteen_sixty_nine_equals_fuel_of_six_fifty_four(self):
        fuel = fuel_from_mass(1969)

        self.assertEqual(fuel, 654)

    def test_sum_list_of_mass_modules(self):
        mass = [12, 12, 1969]
        total_fuel = sum_list_of_mass_modules(mass)

        self.assertEqual(total_fuel, 658)

    def test_total_fuel_from_mass_of_twelve_equals_two(self):
        fuel = total_fuel_from_mass(12)

        self.assertEqual(fuel, 2)

    def test_total_fuel_from_mass_of_100756_is_50346(self):
        fuel = total_fuel_from_mass(100756)

        self.assertEqual(fuel, 50346)
