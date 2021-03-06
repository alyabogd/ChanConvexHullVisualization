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

    def __eq__(self, o) -> bool:
        return self.id == o.id and self.coordinates == o.coordinates


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

    def __len__(self):
        return len(self.dots)

    def __str__(self) -> str:
        return "[{}, {}]".format(self.id, self.dots)

    def __repr__(self) -> str:
        return self.__str__()


class ConvexHull:
    def __init__(self, dots_group, lines):
        # Group object with dots which form the convex hull
        self.dots_group = dots_group
        # Ids of canvas lines, which connect dots from dots_group
        self.lines = lines

    def get_dot(self, index):
        return self.dots_group.dots[index]

    def __len__(self):
        return len(self.dots_group)
