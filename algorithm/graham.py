from visualization.dot import rotate


def get_start_dot(dots):
    """
    Returns a dot which is guaranteed to be in convex hull
    Chosen dot has the lowest x and y-coordinates
    """

    best_dot = dots[0]
    for dot in dots:
        if dot.coordinates[0] < best_dot.coordinates[0]:
            best_dot = dot
            continue
        if dot.coordinates[0] == best_dot.coordinates[0] and dot.coordinates[1] < best_dot.coordinates[1]:
            best_dot = dot

    return best_dot


def get_cmp_for_dot(start_dot):
    def comp_func(a, b):
        angle = rotate(start_dot, a, b)
        if angle != 0:
            return angle

        dist_a = start_dot.get_squared_distance_to(a)
        dist_b = start_dot.get_squared_distance_to(b)
        if dist_a < dist_b:
            return -1
        return 1

    return comp_func


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'

    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K
