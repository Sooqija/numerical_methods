# Interface
import tkinter as tk
import my_style as ms

# Arrays ? is need
import numpy as np

# Charts
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Algorithms
import implicit_method_for_heat_equation as alg


#Main Settings
matplotlib.use("TkAgg")
window = tk.Tk()
# {l, n, _T_, m, a, cur_t, h, tau}
data = {"l": 1.0, "n": 6, "_T_": 1.0, "m": 40, "a": 1.0, "cur_t": 0.0, "h": None, "tau": None} # Default values
var_def = {"длина стержня", "кол-во шагов h разбиения длины стержня", " конечное время нагрева стержня", "количество шагов промежутка времени _T_", "теплопроводность стержня"} # variables definitions
T_1 = []

def clear(): 
    global window
    for part in window.winfo_children():
        part.destroy()

def help(): # INFO
    pass


def get_data():
    global window
    global data
    # instances = ["l", "n"]
    # data = [1.0, 20, 1.0, 1000, 1.0] # [l, n, _T_, m, a]
    names = list(data.keys())
    for i in range(5):
        E_sample = window.nametowidget(names[i])
        if len(E_sample.get()) > 0:
            try:
                data[names[i]] = int(E_sample.get())
            except:
                try:
                    data[names[i]] = float(E_sample.get())
                except:
                    tk.messagebox.showinfo("Error", "Wrong format data")

    data["h"], data["tau"] = alg.calc([data["l"], data["n"], data["_T_"], data["m"]])

def show_chart(x, T_0, T_1):
    global data
    figure = Figure(figsize = (10, 6), dpi = 100)
    plot = figure.add_subplot(111)

    plot.set_xlabel(r"$x$")
    plot.set_ylabel(r"$T$")
    plot.plot(x, T_0, color = "blue") # list(map(abs, T_0))
    plot.plot(x, T_1, color="red") # list(map(abs, T_1))
    plot.legend([r"$\phi(x)$", r"$u(x, T)$"])
    plot.grid()
    canvas = FigureCanvasTkAgg(figure, master = window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().place(x = 10, y = 10)

def change_time(p): # p = [tau, _T_]
    global data
    _T_, tau, time = data["_T_"], data["tau"], data["cur_t"]

    # !
    print("tau = ", tau)
    print(_T_)
    print(time + p * tau)

    if tau == _T_ or time + p * tau > _T_:
        tk.messagebox.showinfo("Error", "Time is above the limit_1")
    elif time + p * tau < 0:
        tk.messagebox.showinfo("Error", "Time is above the limit_2")
    else:
        time += p * tau
    data["cur_t"] = time

    # !
    print(time)

    clear()
    solve()

def first_solvation(): 
    global data

    get_data()

    clear()
    solve()

def fetch_data():
    h = data["h"]
    tau = data["tau"]
    a = data["a"]
    n = data["n"]
    m = data["m"]
    l = data["l"]
    _T_ = data["_T_"]
    time = data["cur_t"]
    return h, tau, a, n, m, l, _T_, time

def solve():
    global data
    global T_1

    Lb_process = tk.Label(window, text="Numerical solvation in progress", font=ms.fontStyle())
    Lb_process.place(x = 450, y = 200)

    h, tau, a, n, m, l, _T_, time = fetch_data()

    T_0, T_1 = alg.solve(h, tau, a, n, m, l, _T_, time, T_1)
    x = [i*h for i in range(n)]

    clear()
    show_chart(x, T_0, T_1)

    B_next = ms.ButtonP(window, name="next", text="Next", command=change_time, p=1)
    B_next.place(x = 1050, y = 550)
    # B_prev = ms.ButtonP(window, name="prev", text=r"Prev {$\tau$}", command=change_time, p=-1)
    # B_prev.place(x = 1000, y = 300)

def main():
# Window
    global window
    ms.set_window(window, "Heat equation solver using implicit finite-difference method")

    Lb_intro = ms.Label(window, name="__intro", text="Enter data of the heat equation")
    Lb_intro.place(x = 400, y = 50)

    # Lb_getinfo = tk.Label(window, text="Definishion parameters of the heat equation", font=ms.fontStyle())
    # Lb_getinfo.place(x = 450, y = 600)

# Buttons
    B_solve = ms.Button(window, name="solve", text="Solve", command=first_solvation)
    B_solve.place(x = 600, y = 550)

    B_help = ms.Button(window, name="help", text="Help", command=help)
    B_help.place(x = 500, y = 550)

# Text
    names = list(data.keys())
    defs = list(var_def)

    Lb_data = []
    for i in range(5):
        Lb_sample = ms.Label(window, name="__{}".format(names[i]), text="{} = ".format(names[i]))
        Lb_sample.place(x = 50, y = (i+3) * 50)
        Lb_data.append(Lb_sample)

        Lb_def_sample = ms.Label(window, name="_{}".format(names[i]), text="    —   {}".format(defs[i]))
        Lb_def_sample.place(x = 200, y = (i+3) * 50)
        Lb_data.append(Lb_def_sample)

    E_data = []
    for i in range(5):
        E_sample = tk.Entry(window, name="{}".format(names[i]), width=7, font=ms.fontStyle())
        E_sample.place(x = 100, y = (i+3) * 50)
        E_data.append(E_sample)

    # E_l = tk.Entry(window, name="l", width=7, font=ms.fontStyle())
    # E_l.place(x = 150, y = 50)

    # E_n = tk.Entry(window, name="n", width = 7, font = ms.fontStyle())
    # E_n.place(x = 150, y = 150)

    window.mainloop()


if __name__ == "__main__":
    main()