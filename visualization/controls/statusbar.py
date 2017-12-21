import tkinter as tk


class StatusBar(tk.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.status_label = tk.Label(self, text="Status bar", padx=5, pady=5)
        self.status_label.grid(row=0, sticky=tk.W)

    def set_status(self, status):
        self.status_label['text'] = status
