import tkinter as tk


class ControlPanel(tk.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.start_button = tk.Button(self, width=20, text="Start")
        self.start_button.grid(row=0, columnspan=2, sticky=tk.N)

        self.reset_button = tk.Button(self, width=20, text="Reset")
        self.reset_button.grid(row=1, columnspan=2)

        # create an empty space
        self.empty_label = tk.Label(self, text="  ", padx=5, pady=5)
        self.empty_label.grid(row=2, columnspan=2)

        self.random_label = tk.Label(self, text="Random dots: ", padx=5, pady=5)
        self.random_label.grid(row=3, column=0)

        self.num_of_dots_entry = tk.Entry(self, width=5)
        self.num_of_dots_entry.insert(0, "30")
        self.num_of_dots_entry.grid(row=3, column=1)

        self.add_points_button = tk.Button(self, width=20, text="Create")
        self.add_points_button.grid(row=4, columnspan=2)

        # create an empty space
        self.empty_label_2 = tk.Label(self, text="  ", padx=5, pady=5)
        self.empty_label_2.grid(row=5, columnspan=2)

        self.speed_label = tk.Label(self, text="Select speed: ", padx=5, pady=0)
        self.speed_label.grid(row=6, columnspan=2, sticky=tk.W)

        self.speed_scale = tk.Scale(self, from_=0.1, to=10, orient=tk.HORIZONTAL, resolution=0.1, length=130)
        self.speed_scale.grid(row=7, columnspan=2)

    def set_start_action(self, callback):
        def action():
            self.start_button.config(state=tk.DISABLED)
            callback()

        self.start_button.config(command=action)

    def set_reset_action(self, callback):
        def action():
            self.start_button.config(state=tk.NORMAL)
            callback()

        self.reset_button.config(command=action)

    def set_random_dots_action(self, callback):
        def action():
            n = int(self.num_of_dots_entry.get())
            callback(n)

        self.add_points_button.config(command=action)

    def get_selected_delay(self):
        print("delay {}".format(1 - int(self.speed_scale.get()) / 10.05))
        return (1 - int(self.speed_scale.get()) / 10.05)
