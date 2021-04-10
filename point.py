import math

class Point:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_x(self):
        return self.x_pos

    def get_y(self):
        return self.y_pos

    def set_x(self, x):
        self.x_pos = x

    def set_y(self, y):
        self.y_pos = y

    def get_tuple(self):
        return (self.x_pos, self.y_pos)

    def point_dist(self, other):
        other_x = other.get_x()
        other_y = other.get_y()
        return math.sqrt((other_x - self.get_x()) ** 2 + (other_y - self.get_y()) ** 2)
