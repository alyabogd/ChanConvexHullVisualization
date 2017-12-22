import tkinter as tk

from visualization.root import Root

if __name__ == "__main__":
    root = tk.Tk()
    main_app = Root(root)
    main_app.mainloop()
