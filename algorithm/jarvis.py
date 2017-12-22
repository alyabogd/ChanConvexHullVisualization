from visualization.dot import rotate


def get_next_dot(dot_index, hull_index, hulls):
    hull = hulls[hull_index]
    if len(hull) > 1:
        return dot_index - 1, hull_index
    return 0, hull_index - 1


def find_leftest_from_hulls(hulls):
    leftest_dot = hulls[0].dots_group.dots[0]
    hull_chosen = 0

    for i, hull in enumerate(hulls):
        # leftest dot in the hull is the first in the list (due to the building algorithm)
        l_dot = hull.dots_group.dots[0]
        if l_dot.coordinates[0] < leftest_dot.coordinates[0] or (
                l_dot.coordinates[0] == leftest_dot.coordinates[0] and
                l_dot.coordinates[1] < leftest_dot.coordinates[1]):
            leftest_dot = l_dot
            hull_chosen = i
    return leftest_dot, hull_chosen


def _prev_and_next_angles(dot, index, hull):
    next_index = (index + 1) % len(hull)
    prev_index = (index - 1 + len(hull)) % len(hull)

    next_angle = rotate(dot, hull.get_dot(index), hull.get_dot(next_index))
    prev_angle = rotate(dot, hull.get_dot(index), hull.get_dot(prev_index))
    return prev_angle, next_angle


def find_rightest_index(dot, hull):
    """
     Returns index of dot in the hull that has the right tangent line from p to hull.
    """

    left = 0
    right = len(hull)

    while right - left > 1:
        m = (left + right) // 2
        m_prev_angle, m_next_angle = _prev_and_next_angles(dot, m, hull)

        if m_next_angle >= 0 and m_prev_angle >= 0:
            return m

        # check which pointer to move
        m_side = rotate(dot, hull.get_dot(left), hull.get_dot(m))

        l_prev_angle, l_next_angle = _prev_and_next_angles(dot, left, hull)

        if m_side > 0 and (l_next_angle < 0 or l_prev_angle == l_next_angle) or (m_side < 0 and m_prev_angle < 0):
            right = m
        else:
            left = m + 1

    return left
