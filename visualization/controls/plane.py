import tkinter as tk

from visualization.dot import Dot, Group


class Plane(tk.Canvas):
    DOT_RADIUS = 3
    COLORS = {
        "Red": "#F44336",
        "Pink": "#E91E63",
        "Purple": "#9C27B0",
        "Deep Purple": "#673AB7",
        "Indigo": "#3F51B5",
        "Blue": "#2196F3",
        "Cyan": "#00BCD4",
        "Teal": "#009688",
        "Green": "#2E7D32",
        "Light Green": "#8BC34A",
        "Lime": "#9E9D24",
        "Yellow": "#F9A825",
        "Amber": "#FF6F00",
        "Orange": "#FF9800",
        "Deep Orange": "#FF5722",
        "Brown": "#795548",
        "Blue Grey": "#607D8B"
    }

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

    def create_segment(self, dot_a, dot_b, color="black", **kwargs):
        line_id = self.create_line(dot_a.coordinates[0] + self.DOT_RADIUS,
                                   dot_a.coordinates[1] + self.DOT_RADIUS,
                                   dot_b.coordinates[0] + self.DOT_RADIUS,
                                   dot_b.coordinates[1] + self.DOT_RADIUS,
                                   fill=color,
                                   **kwargs)
        return line_id

    def get_all_dots(self):
        all_coordinates = [self.coords(p)[:2] for p in self.points]
        return [Dot(i, coords) for i, coords in zip(self.points, all_coordinates)]

    def _change_color(self, id, color):
        self.itemconfig(id, fill=color, outline=color)

    def color_groups(self, groups):
        color_keys = list(self.COLORS.keys())

        for group in groups:
            color = self.COLORS[color_keys[group.id % len(self.COLORS)]]
            for dot in group.dots:
                self._change_color(dot.id, color)

    def emphasize_dot(self, dot):
        self.itemconfig(dot.id, width=3)
        self.itemconfig(dot.id, outline="black")

    def remove_emphasize_dot(self, dot):
        self.itemconfig(dot.id, width=1)
        fill_color = self.itemcget(dot.id, 'fill')
        self.itemconfig(dot.id, outline=fill_color)

    def emphasize_group(self, group):
        for dot in group.dots:
            self.itemconfig(dot.id, width=7)

    def remove_emphasize_group(self, group):
        for dot in group.dots:
            self.itemconfig(dot.id, width=1)

    def emphasize_line(self, *line_ids):
        for line_id in line_ids:
            self.itemconfig(line_id, width=3)

    def remove_emphasize_line(self, *line_ids):
        for line_id in line_ids:
            self.itemconfig(line_id, width=1)

    def apply(self, *ids, **kwargs):
        for id in ids:
            self.itemconfig(id, **kwargs)
