import tkinter as tk
import time

from algorithm.graham import cmp_to_key, get_cmp_for_dot, get_start_dot
from visualization.controls.control_panel import ControlPanel
from visualization.controls.plane import Plane
from visualization.controls.statusbar import StatusBar
from visualization.dot import Group, rotate


class Root(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self._configure_window()
        self._initialize_controls(master)

        self.hulls = []

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
        # divide initial dots into groups
        groups = Root._divide_into_groups(dots, batch_size)
        self.plane.color_groups(groups)

        # build convex hull over each hull using Graham scan
        for group in groups:
            self._show_graham_scan(group)
            time.sleep(1)

        return True

    def _show_graham_scan(self, group):
        self.status_global.set_status("Building convex hull for group {} using Graham scan".format(group.id + 1))
        self.plane.emphasize_group(group)

        self._graham_scan_steps(group.dots, 0.15)

        self.plane.remove_emphasize_group(group)

    def _graham_scan_steps(self, dots, delay):
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

                self.plane.emphasize_line(lines[-1])
                self.plane.emphasize_line(lines[-2])
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
        return hull

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
