import tkinter as tk
import time

from algorithm.graham import cmp_to_key, get_cmp_for_dot, get_start_dot
from algorithm.jarvis import find_leftest_from_hulls, find_rightest_index, get_next_dot
from visualization.controls.control_panel import ControlPanel
from visualization.controls.plane import Plane
from visualization.controls.statusbar import StatusBar
from visualization.dot import Group, rotate, ConvexHull


class Root(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self._configure_window()
        self._initialize_controls(master)

        self.graham_hulls = []

    def _configure_window(self):
        self.master.title("Chan's algorithm visualization")
        self.master.geometry("900x800")
        self.master.resizable(False, False)

    def _initialize_controls(self, master):
        self.label = tk.Label(master, text="Chan's algorithm", padx=5, pady=5)
        self.label.grid(row=0)

        # status bar
        self.status_global = StatusBar(height=50, width=900)
        self.status_global.grid(row=1, columnspan=2, sticky=tk.W)

        # control panel
        self.control_panel = ControlPanel(width=300)
        self.control_panel.grid(row=2, column=0)
        self.control_panel.set_start_action(self._build_convex_hull)

        # canvas with dots
        self.plane = Plane(width=600, height=900, background="white", highlightbackground="black", highlightthickness=1)
        self.plane.grid(row=2, column=1)
        self.plane.bind("<Button-1>", lambda event: self.plane.create_dot(event.x, event.y))

    def _build_convex_hull(self):
        dots = self.plane.get_all_dots()

        for i in range(1, len(dots)):
            batch_size = min(2 ** (2 ** i), len(dots))
            is_build = self._solve_for_batch_size(dots, batch_size)
            if is_build:
                return

    def _solve_for_batch_size(self, dots, batch_size):
        # delete existing hulls if any
        for hull in self.graham_hulls:
            self.plane.delete(*hull.lines)
        self.graham_hulls.clear()

        # divide initial dots into groups
        groups = Root._divide_into_groups(dots, batch_size)
        self.plane.color_groups(groups)

        # build convex hull over each hull using Graham scan
        for group in groups:
            hull = self._perform_graham_scan(group)
            self.graham_hulls.append(hull)
            time.sleep(1)

        time.sleep(2)
        print("starting Jarvis")
        is_build, line_ids, hull = self._perform_jarvis_march(batch_size)
        if not is_build:
            self.plane.delete(*line_ids)
        return is_build

    def _perform_graham_scan(self, group):
        self.status_global.set_status(
            "Building convex hull for group {} using Graham scan algorithm".format(group.id + 1))
        self.plane.emphasize_group(group)

        hull = self._graham_scan_steps(group, delay=0.15)

        self.plane.remove_emphasize_group(group)
        return hull

    def _graham_scan_steps(self, group, delay=.0):
        dots = group.dots

        start_dot = get_start_dot(dots)
        self.plane.emphasize_dot(start_dot)
        self.plane.update()
        time.sleep(delay)

        self.plane.remove_emphasize_dot(start_dot)

        # sort dots by 'rightness' (cw order)
        dots.remove(start_dot)
        dots.sort(key=cmp_to_key(get_cmp_for_dot(start_dot)))
        dots.insert(0, start_dot)

        hull = []
        lines = []

        hull.append(dots[0])
        if len(dots) == 1:
            return hull

        hull.append(dots[1])
        line_id = self.plane.create_segment(dots[0], dots[1])
        lines.append(line_id)
        self.plane.update()
        time.sleep(delay)

        for i in range(2, len(dots)):
            # try adding i-th dot
            while len(hull) >= 2 and rotate(hull[-1], hull[-2], dots[i]) <= 0:
                lines.append(self.plane.create_segment(hull[-1], dots[i]))
                self.plane.update()
                time.sleep(delay)

                self.plane.emphasize_line(lines[-1], lines[-2])
                self.plane.update()
                time.sleep(delay)

                hull.pop()

                self.plane.delete(lines[-1], lines[-2])
                lines.pop()
                lines.pop()
                self.plane.update()
                time.sleep(delay)

            hull.append(dots[i])
            lines.append(self.plane.create_segment(hull[-1], hull[-2]))
            self.plane.update()
            time.sleep(delay)

        lines.append(self.plane.create_segment(hull[0], hull[-1]))
        self.plane.update()

        return ConvexHull(Group(group.id, hull), lines)

    def _perform_jarvis_march(self, max_steps, delay=1):
        # blur existing lines on the screen
        for hull in self.graham_hulls:
            self.plane.apply(*hull.lines, fill="grey")
        self.plane.update()
        time.sleep(delay)

        # find the leftest dot - start dot for Jarvis march
        # and a hull, which this dot belongs to
        self.status_global.set_status("Find the leftest dot in the input set")
        start_dot, active_hull_index = find_leftest_from_hulls(self.graham_hulls)

        self.plane.emphasize_dot(start_dot)
        time.sleep(delay)

        self.plane.remove_emphasize_dot(start_dot)

        hull_line_ids = []
        hull = [start_dot]

        current_dot = start_dot
        current_dot_index = 0
        for i in range(max_steps):
            self.status_global.set_status("{} step from {}".format(i + 1, max_steps))
            dot_index, hull_index = self._perform_jarvis_march_step(current_dot_index, active_hull_index, delay)

            dot = self.graham_hulls[hull_index].get_dot(dot_index)
            hull_line_ids.append(self.plane.create_segment(current_dot, dot, color="red", width=5))
            self.plane.update()
            time.sleep(delay)

            current_dot_index = dot_index
            active_hull_index = hull_index
            current_dot = dot
            hull.append(current_dot)

            if current_dot == hull[0]:
                break

        return hull[-1] == hull[0], hull_line_ids, hull

    def _perform_jarvis_march_step(self, base_dot_index, base_hull_index, delay):
        lines = []
        base_dot = self.graham_hulls[base_hull_index].get_dot(base_dot_index)

        next_dot_index, next_hull_index = get_next_dot(base_dot_index, base_hull_index, self.graham_hulls)
        next_dot = self.graham_hulls[base_hull_index].get_dot(next_dot_index)
        next_hull_index = base_hull_index

        lines.append(self.plane.create_segment(base_dot, next_dot))
        self.plane.update()
        time.sleep(delay)

        for i, hull in enumerate(self.graham_hulls):
            if i == base_hull_index:
                continue
            dot_index = find_rightest_index(base_dot, hull)

            lines.append(self.plane.create_segment(base_dot, hull.get_dot(dot_index)))
            self.plane.update()
            time.sleep(delay)

            if rotate(base_dot, next_dot, hull.get_dot(dot_index)) < 0:
                next_dot = hull.get_dot(dot_index)
                next_dot_index = dot_index
                next_hull_index = i

        self.plane.delete(*lines)
        lines.clear()

        return next_dot_index, next_hull_index

    @staticmethod
    def _divide_into_groups(dots, batch_size):
        groups = []

        start = 0
        end = batch_size
        i = 0

        while start < len(dots):
            groups.append(Group(i, dots[start:end]))
            start = end
            end = min(end + batch_size, len(dots))
            i += 1

        return groups


if __name__ == "__main__":
    root = tk.Tk()
    main_app = Root(root)
    main_app.mainloop()
