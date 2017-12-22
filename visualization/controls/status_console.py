import tkinter as tk


class StatusConsole(tk.Text):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.template = "\n {} \n"

    def print_status(self, status):
        self.insert('1.0', self.template.format(status))
