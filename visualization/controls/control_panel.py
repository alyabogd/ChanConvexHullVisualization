import tkinter as tk


class ControlPanel(tk.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.start_button = tk.Button(self, text="Start")
        self.start_button.grid(row=0, sticky=tk.N)

    def set_start_action(self, callback):
        def action():
            self.start_button.config(state=tk.DISABLED)
            callback()
        self.start_button.config(command=action)
