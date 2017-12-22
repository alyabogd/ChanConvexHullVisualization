import tkinter as tk


class StatusBar(tk.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.batch_size_label = tk.Label(self, text="Batch size: -")
        self.batch_size_label.grid(row=0, columnspan=2, sticky=tk.W)

        self.status_label = tk.Label(self, text="Click on the screen to add a dot", padx=5, pady=5)
        self.status_label.grid(row=1, column=0, sticky=tk.W)

        self.sub_status_label = tk.Label(self, text="", padx=5, pady=5)
        self.sub_status_label.grid(row=1, column=1, sticky=tk.W)

    def set_status(self, status):
        self.status_label['text'] = status

    def set_default_status(self):
        self.status_label['text'] = "Click on the screen to add a dot"

    def set_batch_size(self, size):
        self.batch_size_label['text'] = "Batch size: {}".format(size)

    def set_sub_status(self, status):
        self.sub_status_label['text'] = status
