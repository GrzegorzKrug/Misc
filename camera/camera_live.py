from tkinter import (
    Frame, Grid,
    N, S, W, E,
    Button, Label)

import tkinter as tk
from tkinter import messagebox

LARGE_FONT = ("Verdana", 12)


class Window(Frame):
    def __init__(self, master=None, pack_side=None):
        super().__init__(master)

        # self.master = master

        hei = Frame.winfo_height(self)
        wid = Frame.winfo_width(self)
        self.pack(side=pack_side)


def add_button(_frame, text, fg, side=None, fill=None,
               row=0, col=0, sticky=None):
    but = Button(_frame, text=text, fg=fg)
    but.grid(row=row, column=col, sticky=sticky)
    # but.pack(side=side, fill='both')
    # but.pack(expand=1)
    return but


def hello_world():
    messagebox.showinfo("Hello")


if __name__ == "__main__":
    root = tk.Tk()

    frame = Frame()
    frame.pack(expand=True, fill='both')
    # Grid.columnconfigure(root, 0, weight=1)

    # frame.grid_rowconfigure(0, weight=1)
    # frame.grid_columnconfigure(0, weight=1)
    buttons = {(2, 1), (2, 2), (2, 3), (3, 2)}
    for r in range(8):
        for c in range(8):
            if (r, c) in buttons:
                continue
            padx = 5
            pady = 2
            Label(frame, text=f"R_{r} C_{c}", relief='solid', borderwidth=2).grid(row=r, column=c, sticky='nwse',
                                                                                  ipadx=padx, ipady=pady)

    for x in range(8):
        Grid.columnconfigure(frame, x, weight=1)

    for y in range(8):
        Grid.rowconfigure(frame, y, weight=1)

    add_button(frame, 'Blue', 'blue', row=2, col=1, sticky="nwse").grid(rowspan=2)
    add_button(frame, 'Green', 'green', row=2, col=2, sticky="nwse").configure(command=hello_world)
    add_button(frame, 'Black', 'black', row=2, col=3, sticky="nwse").grid(rowspan=2)
    add_button(frame, 'Red', 'red', row=3, col=2, sticky="nwse")

    # Grid.rowconfigure(frame, 0, weight=1)
    # Grid.columnconfigure(frame, 0, weight=1)
    # Grid.rowconfigure(frame, 1, weight=1)
    # Grid.columnconfigure(frame, 1, weight=1)

    # frame.grid(row=0, column=0, sticky="n")
    # lower_frame.grid(row=0, column=0, sticky=N + S + E + W)
    # grid = Frame(frame)

    # grid.grid(sticky=N + S + E + W, column=0, row=7, columnspan=2)

    root.mainloop()
