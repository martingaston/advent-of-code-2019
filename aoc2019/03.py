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

if __name__ == "__main__":
    wire_paths = list(map(lambda wire_path: wire_path.split(","), read_file_to_list("input/03.txt")))
    wire_points = []

    for wire_path in wire_paths:
        wire_points.append(move_list_of_movements(wire_path))

    intersections = find_intersections(wire_points[0], wire_points[1])
    distances_from_origin = [manhattan_distance(Point(0,0), intersection) for intersection in intersections]
    print(min(distances_from_origin))

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
