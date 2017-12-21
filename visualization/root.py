import tkinter as tk

from visualization.controls.control_panel import ControlPanel
from visualization.controls.plane import Plane
from visualization.controls.statusbar import StatusBar


class Root(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self._configure_window()
        self._initialize_controls(master)

    def _configure_window(self):
        self.master.title("Chan's algorithm visualization")
        self.master.geometry("900x800")
        self.master.resizable(False, False)

    def _initialize_controls(self, master):
        self.label = tk.Label(master, text="Chan's algorithm", padx=5, pady=5)
        self.label.grid(row=0)

        # status bar
        self.status_global = StatusBar(height=50, width=900)
        self.status_global.grid(row=1, sticky=tk.W)

        # control panel
        self.control_panel = ControlPanel(width=300)
        self.control_panel.grid(row=2, column=0)
        self.control_panel.set_start_action(lambda: 1 + 1)

        # canvas with dots
        self.plane = Plane(width=600, height=900, background="white", highlightbackground="black", highlightthickness=1)
        self.plane.grid(row=2, column=1)
        self.plane.bind("<Button-1>", lambda event: self.plane.create_dot(event.x, event.y))


if __name__ == "__main__":
    root = tk.Tk()
    main_app = Root(root)
    main_app.mainloop()
