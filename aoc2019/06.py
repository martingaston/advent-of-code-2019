import unittest
import collections


def steps_to_root(node, nodes):
    root = "COM"
    count = 1

    while nodes[node] != root:
        count += 1
        node = nodes[node]

    return count


def parse_orbit_map(orbit_map):
    orbit_nodes = {}

    for orbit_node in orbit_map:
        orbiter, orbits = orbit_node.split(")")
        if orbits not in orbit_nodes:
            orbit_nodes[orbits] = orbiter

    return orbit_nodes


def parse_bidirectional_map(orbit_map):
    orbit_nodes = {}

    for orbit_node in orbit_map:
        orbiter, orbits = orbit_node.split(")")
        if orbiter not in orbit_nodes:
            orbit_nodes[orbiter] = [orbits]
        else:
            orbit_nodes[orbiter].append(orbits)

        if orbits not in orbit_nodes:
            orbit_nodes[orbits] = [orbiter]
        else:
            orbit_nodes[orbits].append(orbiter)

    return orbit_nodes


def bfs(start, finish, bidirectional_map):
    seen = set()
    seen.add(start)
    queue = collections.deque([])
    queue.append((bidirectional_map[start], 1))

    while finish not in seen:
        node, steps = queue.popleft()

        for child in node:
            if child in seen:
                continue

            seen.add(child)
            if child == finish:
                return steps

            queue.append((bidirectional_map[child], steps + 1))


def count_orbits(orbit_map):
    orbit_nodes = parse_orbit_map(orbit_map)
    return sum([steps_to_root(orbit_node, orbit_nodes) for orbit_node in orbit_nodes])


if __name__ == "__main__":
    with open("input/06.txt") as f:
        orbit_map = f.read().splitlines()
        bidirectional_map = parse_bidirectional_map(orbit_map)
        shortest = bfs("YOU", "SAN", bidirectional_map)
        print(
            f"the shortest number of orbit stops between YOU and SAN is: {shortest - 2}"
        )
        print(
            f"the total direct and indirect orbits of the orbit map are: {count_orbits(orbit_map)}"
        )


class Test(unittest.TestCase):
    def test_functional_test_to_check_multiple_branches(self):
        orbit_map = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L",
        ]
        orbits = count_orbits(orbit_map)

        self.assertEqual(42, count_orbits(orbit_map))

    def test_shortest_path_to_santa(self):
        orbit_map = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L",
            "K)YOU",
            "I)SAN",
        ]

        bidirectional_map = parse_bidirectional_map(orbit_map)
        shortest = bfs("YOU", "SAN", bidirectional_map)

        self.assertEqual(4, shortest - 2)
