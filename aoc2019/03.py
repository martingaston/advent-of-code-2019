import unittest
from functools import reduce
from itertools import accumulate
from utils import read_file_to_list

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        return Point(x=self.x + x, y=self.y + y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y

        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Move:
    def __init__(self, movement):
        self.x = 0
        self.y = 0
        self.direction = None
        self.amount = 0

        if type(movement) != str or len(movement) < 2:
            raise ValueError(f"Invalid movement direction provided: {movement}")

        direction = self.__get_direction(movement[0])
        amount = self.__verify_amount(movement[1:])

        self.x = self.x * amount
        self.y = self.y * amount

    def __get_direction(self, direction):
        self.direction = direction

        if direction == "U":
            self.y = 1
        elif direction == "D":
            self.y = -1
        elif direction == "L":
            self.x = -1
        elif direction == "R":
            self.x = 1
        else:
            raise ValueError(f"Movement must be U, D, L or R: {movement} provided")

    def __verify_amount(self, amount):
        try:
            self.amount = int(amount)
            return int(amount)
        except ValueError:
            raise ValueError(f"Movement amount must be an integer: {amount} provided")

def find_intersections(points_one, points_two):
    intersections = set(points_one) & set(points_two)
    intersections.discard(Point(0,0))

    return list(intersections)

def manhattan_distance(point_a, point_b):
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)

def move_to_next_point(point, move):
    movement = [point]
    distance = abs(move.amount)

    for _ in range(distance):
        last_point = movement[-1]
        sign = 1 if move.direction in ("R", "U") else -1
        x = last_point.x + 1 * sign if move.direction in ("L", "R") else last_point.x
        y = last_point.y + 1 * sign if move.direction in ("U", "D") else last_point.y

        movement.append(Point(x, y))

    return movement

def move_list_of_movements(movements):
    origin_point = Point(0,0)

    current_point = origin_point
    points = [origin_point]
    for movement in movements:
        next_point = move_to_next_point(current_point, Move(movement))
        points.extend(next_point[1:])
        current_point = next_point[-1]

    return points

def count_steps(wire, intersection_index):
    return len(wire[:intersection_index])

if __name__ == "__main__":
    wire_paths = list(map(lambda wire_path: wire_path.split(","), read_file_to_list("input/03.txt")))
    wire_points = []

    for wire_path in wire_paths:
        wire_points.append(move_list_of_movements(wire_path))

    intersections = find_intersections(wire_points[0], wire_points[1])
    steps = [[count_steps(path, path.index(intersection)) for intersection in intersections] for path in wire_points]
    fewest_steps = min(first_wire + second_wire for (first_wire, second_wire) in zip(steps[0], steps[1]))
    distances_from_origin = [manhattan_distance(Point(0,0), intersection) for intersection in intersections]
    print(min(distances_from_origin))
    print(fewest_steps)

class Test(unittest.TestCase):
    def test_unittest_is_working(self):
        self.assertEqual(10, 5 + 5)

    def test_point_can_be_constructed(self):
        point = Point(x=1, y=7)

        self.assertEqual(1, point.x)
        self.assertEqual(7, point.y)

    def test_point_can_return_a_new_moved_point(self):
        original_point = Point(x=1, y=7)
        moved_point = original_point.move(x=5, y=-6)

        self.assertEqual(6, moved_point.x)
        self.assertEqual(1, moved_point.y)

    def test_moved_point_returns_a_new_point(self):
        original_point = Point(x=1, y=7)
        moved_point = original_point.move(x=5, y=-6)

        self.assertNotEqual(original_point, moved_point)

    def test_move_can_parse_up_input(self):
        moved_up = Move("U14")

        self.assertEqual(moved_up.y, 14)
        self.assertEqual(moved_up.x, 0)

    def test_move_can_parse_down_input(self):
        moved_up = Move("D14")

        self.assertEqual(moved_up.y, -14)
        self.assertEqual(moved_up.x, 0)

    def test_move_can_parse_left_input(self):
        moved_up = Move("L14")

        self.assertEqual(moved_up.y, 0)
        self.assertEqual(moved_up.x, -14)

    def test_move_can_parse_right_input(self):
        moved_up = Move("R14")

        self.assertEqual(moved_up.y, 0)
        self.assertEqual(moved_up.x, 14)

    def test_intersections_can_find_points(self):
        points_one = [Point(0, 5)]
        points_two = [Point(0, 3), Point(0, 4), Point(0, 5)]

        intersections = find_intersections(points_one, points_two)

        self.assertEqual(intersections, [Point(0, 5)])

    def test_manhattan_point(self):
        point_a = Point(x=0,y=0)
        point_b = Point(x=6,y=6)

        distance = manhattan_distance(point_a, point_b)

        self.assertEqual(12, distance)

    def test_manhattan_point_with_negatives(self):
        point_a = Point(x=0,y=0)
        point_b = Point(x=-6,y=-6)

        distance = manhattan_distance(point_a, point_b)

        self.assertEqual(12, distance)

    def test_move_to_next_point_returns_a_list_of_points(self):
        steps_to_next_point = move_to_next_point(Point(1,0), Move("R1"))

        self.assertEqual([Point(1,0), Point(2,0)], steps_to_next_point)

    def test_move_to_next_point_can_move_more_than_one_step(self):
        steps_to_next_point = move_to_next_point(Point(2,1), Move("D2"))

        self.assertEqual([Point(2,1), Point(2,0), Point(2,-1)], steps_to_next_point)

    def test_move_to_next_point_can_move_more_than_one_movement(self):
        points = move_list_of_movements(["R2", "U2", "L2", "D2"])

        self.assertEqual([Point(0,0), Point(1, 0), Point(2,0), Point(2,1), Point(2,2), Point(1,2), Point(0,2), Point(0,1), Point(0,0)], points)

    def test_can_count_steps(self):

        wire = [Point(0,0), Point(0,1), Point(0,2), Point(0,3), Point(0,4), Point(0,5), Point(1,5), Point(2,5), Point(3,5), Point(4,5), Point(5,5)]
        intersection_index = 10

        steps = count_steps(wire, intersection_index)

        self.assertEqual(10, steps)

    def test_can_find_fewest_steps_example_one(self):
        wires = [wire.split(",") for wire in ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]]
        paths = [move_list_of_movements(wire) for wire in wires]
        intersections = find_intersections(paths[0], paths[1])

        steps = [[count_steps(path, path.index(intersection)) for intersection in intersections] for path in paths]
        fewest_steps = min(first_wire + second_wire for (first_wire, second_wire) in zip(steps[0], steps[1]))

        self.assertEqual(610, fewest_steps)

    def test_can_find_fewest_steps_example_two(self):
        wires = [wire.split(",") for wire in ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]]
        paths = [move_list_of_movements(wire) for wire in wires]
        intersections = find_intersections(paths[0], paths[1])

        steps = [[count_steps(path, path.index(intersection)) for intersection in intersections] for path in paths]
        fewest_steps = min(first_wire + second_wire for (first_wire, second_wire) in zip(steps[0], steps[1]))

        self.assertEqual(410, fewest_steps)
