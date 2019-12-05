import unittest

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Test(unittest.TestCase):
    def test_unittest_is_working(self):
        self.assertEqual(10, 5 + 5)

    def test_point_can_be_constructed(self):
        point = Point(x=1, y=7)

        self.assertEqual(1, point.x)
        self.assertEqual(7, point.y)
