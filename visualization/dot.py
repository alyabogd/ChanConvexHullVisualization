class Dot:
    def __init__(self, id, coordinates):
        self.id = id
        self.coordinates = coordinates

    def get_squared_distance_to(self, other):
        res = 0
        for c, other_c in zip(self.coordinates, other.coordinates):
            res += (c - other_c) ** 2
        return res

    def __str__(self) -> str:
        return "[{}, {}]".format(self.id, self.coordinates)

    def __repr__(self) -> str:
        return self.__str__()


# AB -> AC
# == 0: collinear vectors
#  > 0: 'left turn' ccw
#  < 0: 'right turn' cw
def rotate(a, b, c):
    angle = ((b.coordinates[0] - a.coordinates[0]) * (c.coordinates[1] - a.coordinates[1]) -
             (b.coordinates[1] - a.coordinates[1]) * (c.coordinates[0] - a.coordinates[0]))
    if angle > 0:
        return 1
    if angle < 0:
        return -1
    return 0


class Group:
    def __init__(self, id, dots):
        self.id = id
        self.dots = dots

    def __str__(self) -> str:
        return "[{}, {}]".format(self.id, self.dots)

    def __repr__(self) -> str:
        return self.__str__()
