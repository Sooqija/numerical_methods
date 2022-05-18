import tkinter as tk
import tkinter.font
from functools import partial

#Style
def fontStyle():
    return tkinter.font.Font(family="lucida grande bold", size=18)

def global_background(num):
    if num == 1:
        return "moccasin"
        # return "Steelblue1"

# fontStyle_coordinate=tk.font.Font(family="Arial", size=12)

def set_window(window : tk.Tk, text : str):
    window.geometry('1280x720')
    window.title(text)
    window.configure(background=global_background(1))

def Button(window, name, text, command):
    B_temp = tk.Button(window,
                name=name,
                text=text,
                command = command,
                width = 6,
                height = 1,
                compound = tkinter.CENTER,
                font = fontStyle(),
                background = "sienna",
                foreground="white",
                highlightbackground = "black",
                relief = "solid")

    return B_temp

def ButtonP(window, name, text, command, p):
    B_temp = tk.Button(window,
                name=name,
                text=text,
                command = partial(command, p),
                width = 6,
                height = 1,
                compound = tkinter.CENTER,
                font = fontStyle(),
                background = "LimeGreen",
                highlightbackground = "black",
                relief = "solid")

    return B_temp

def Label(window, name="label", text=""):
    L_temp = tk.Label(window,
                      name=name,
                      text=text,
                      font=fontStyle(),
                      background=global_background(1))

    return L_temp

def LabelT(window, text=""):
    L_temp = tk.Label(window,
                      text=text,
                      font=fontStyle(),
                      background=global_background(1),
                      justify=tk.LEFT)

    return L_temp


def LabelLink(window, text="", callback=None):
    L_temp = tk.Label(window,
                      text=text,
                      font=fontStyle(),
                      background=global_background(1),
                      fg="blue",
                      cursor="hand2")

    L_temp.bind("<Button-1>", callback)

    return L_temp