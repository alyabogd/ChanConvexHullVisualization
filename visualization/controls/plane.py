import tkinter as tk

from visualization.dot import Dot


class Plane(tk.Canvas):
    DOT_RADIUS = 3

    def __init__(self, **kw):
        super().__init__(**kw)
        self.points = []

    def create_dot(self, x, y, color="black"):
        point_id = self.create_oval(x - self.DOT_RADIUS,
                                    y - self.DOT_RADIUS,
                                    x + self.DOT_RADIUS,
                                    y + self.DOT_RADIUS,
                                    fill=color)
        self.points.append(point_id)
        return point_id

    def get_all_dots(self):
        all_coordinates = [self.coords(p)[:2] for p in self.points]
        return [Dot(i, coords) for i, coords in zip(self.points, all_coordinates)]

