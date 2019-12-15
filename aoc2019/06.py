import unittest


def count_orbits(orbit_map):
    space = {}
    for orbit in orbit_map:
        orbiting, orbiter = orbit.split(")")
        if orbiting not in space:
            space[orbiting] = []
            space[orbiting].append(orbiter)
        else:
            space[orbiting].append(orbiter)

    print(space)

    return len(orbit_map), max(0, len(orbit_map) - 1)


class Test(unittest.TestCase):
    def test_is_working(self):
        self.assertEqual(3, 2 + 1)

    def test_center_of_mass_has_no_orbits(self):
        orbits = count_orbits([])

        self.assertEqual(orbits, (0, 0))

    def test_one_object_has_one_direct_orbit(self):
        orbit_map = ["COM)B"]
        orbits = count_orbits(orbit_map)

        direct_orbits, indirect_orbits = count_orbits(orbit_map)

        self.assertEqual(1, direct_orbits)
        self.assertEqual(0, indirect_orbits)

    def test_two_objects_have_two_direct_orbits_and_one_indirect_orbit(self):
        orbit_map = ["COM)B", "B)C"]
        orbits = count_orbits(orbit_map)

        direct_orbits, indirect_orbits = count_orbits(orbit_map)

        self.assertEqual(2, direct_orbits)
        self.assertEqual(1, indirect_orbits)

    def test_three_objects_have_three_direct_orbits_and_two_indirect_orbits(self):
        orbit_map = ["COM)B", "B)C", "C)D"]
        orbits = count_orbits(orbit_map)

        direct_orbits, indirect_orbits = count_orbits(orbit_map)

        self.assertEqual(3, direct_orbits)
        self.assertEqual(2, indirect_orbits)

    def test_multiple_objects_can_orbit_an_object(self):
        orbit_map = ["COM)B", "B)C", "C)D", "B)E"]
        orbits = count_orbits(orbit_map)

        direct_orbits, indirect_orbits = count_orbits(orbit_map)

        self.assertEqual(4, direct_orbits)
        self.assertEqual(5, indirect_orbits)
