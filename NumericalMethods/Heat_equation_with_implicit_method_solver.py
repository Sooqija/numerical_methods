# Interface
import tkinter as tk
import my_style as ms
import webbrowser
# Charts
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Algotithms
import implicit_method_for_heat_equation as alg
import numpy as np
from PIL import Image, ImageTk

def increase():
    global step
    if step < tmsteps - 1:
        step += 1
    return step

def last():
    global step
    while step < tmsteps - 2:
        increase()
    return step

def initstep():
    global step
    step = 0
    return step

VarDef = ["Длинна стержня",
          "Конечное время воздействия",
          "Размер шага сетки по координате x",
          "Размер шага сетки по координате t",
          "Теплопроводность стержня"]

def ClearAll():
    global window
    for part in window.winfo_children():
        part.destroy()

def ThroughReport(event):
    webbrowser.open_new(r"https://1drv.ms/w/s!AuklzTu4sjCrgUwweyhyq7KQ635f?e=nLffVW")

def Help():
    ClearAll()
    Lb_info = ms.LabelT(window,
    text="\
          The general form of heat equation \n \
          \n \
          u'_{t} = a**2 u''_{xx} + f(x, t), where \n \
          \n \
          a - diffusitivity of the rod, const \n \
          x - point on the rod in [0, l], l - length of the rod \n \
          t - time in [0, _T_]\n \
          u(x, t) - temperature in rod at position x, time t \n \
          \n \
          Initial temperature profile \n \
          u(x, 0) = phi(x) for x = (0, l) \n \
          \n \
          Initial boundary conditions: \n \
              1. u(0, t) = T for t > 0 \n \
              2. u'_{x}(0, t) = 0 \n \
              3. u'_{x}(l, t) = 0 \n \
          \n \
          Other parameters: \n \
              n - number of steps for x, then h = l / n \n \
              m - number of steps for t, then tau = _T_ / m \n \
          \n \
              f(x, t) =  1 + cos(pi * x) \n \
              phi(x) = 1 + cos(2*pi*x) \
    ")
    Lb_info.place(x = 300, y = 10)
    B_back = ms.Button(window, "back", "Back", main)
    B_back.place(x = 1050, y = 500)
    Lb_link = ms.LabelLink(window, text="download report", callback=report)
    Lb_link.place(x = 950, y = 600)

def ReadData():
    global length, time_end, h, tau, a
    try:
        length = float(window.nametowidget(Names[0]).get())
        time_end = float(window.nametowidget(Names[1]).get())
        h = float(window.nametowidget(Names[2]).get())
        tau = float(window.nametowidget(Names[3]).get())
        a = float(window.nametowidget(Names[4]).get())
    except:
        tk.messagebox.showinfo("Error", "Wrong format of data")

def Solve(_):
    global TotalTemp, length, h, time_end, tau, xnsteps, tmsteps, xCoord, tCoord, step, a
    ReadData()
    xnsteps = int(length / h)
    tmsteps = int(time_end / tau)
    xCoord = [i*h for i in range(xnsteps)]
    tCoord = [j*tau for j in range(tmsteps)]
    TotalTemp = [0] * tmsteps
    for j in range(tmsteps):
        TotalTemp[j] = [0] * xnsteps
    for i, x in enumerate(xCoord):
        TotalTemp[0][i] = alg.InitialConditions(x, length)

    TotalTemp = alg.ImplicitMethod(step, TotalTemp, length, time_end, h, tau, a, xnsteps, tmsteps, xCoord, tCoord)

    ShowChart()

def ShowChart():
    figure = Figure(figsize = (9, 5), dpi = 100)
    plot = figure.add_subplot(111)
    plot.set_xlabel(r"distance m")
    plot.set_ylabel(r"Temperature $\degree$ C")
    plot.plot(xCoord, TotalTemp[step], color = "blue")
    plot.plot(xCoord, TotalTemp[step+1], color = "green")
    plot.legend([r"$\varphi(x)$", r"$u(x, T)$"])
    plot.grid()
    canvas = FigureCanvasTkAgg(figure, master = window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().place(x = 25, y = 200)

def main():
    # Window
    ClearAll()
    ms.set_window(window, "Heat equation solver using implicit finite-difference method")
    Lb_intro = ms.Label(window, name="__intro", text="Введите значения параметров уравнения теплопроводности")
    Lb_intro.place(x = 50, y = 0)

    # Buttons
    B_help = ms.Button(window, name="help", text="Help", command=Help)
    B_help.place(x = 960, y = 260)
    B_solve = ms.Button(window, name="solve", text="Solve", command=lambda:Solve(initstep()))
    B_solve.place(x = 960, y = 370)
    B_next = ms.Button(window, name="next", text="Next", command=lambda:Solve(increase()))
    B_next.place(x = 960, y = 480)
    B_final = ms.Button(window, name="final", text="Final", command=lambda:Solve(last()))
    B_final.place(x = 960, y = 590)

    # Text
    Lb_data = []
    for i in range(5):
        Lb_sample = ms.Label(window, name="__{}".format(Names[i]), text="{}    =    ".format(Names[i]))
        Lb_sample.place(x = 50, y = (i+1) * 40)
        Lb_data.append(Lb_sample)

        Lb_def_sample = ms.Label(window, name="_{}".format(Names[i]), text="   -   {}".format(VarDef[i]))
        Lb_def_sample.place(x = 300, y = (i+1) * 40)
        Lb_data.append(Lb_def_sample)

    E_data = []
    Values = [1.0, 1.0, 0.01, 0.025, 1.0]
    for i in range(5):
        E_sample = tk.Entry(window, name="{}".format(Names[i]), width=7, font=ms.fontStyle())
        E_sample.insert(0, str(Values[i]))
        E_sample.place(x = 200, y = (i+1) * 40)
        E_data.append(E_sample)

    canvas = tk.Canvas(window, width=400, height=110)
    image = Image.open("e:/Python_Programs/NumericalMethods/phi.png")
    photo = ImageTk.PhotoImage(image)
    image = canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.place(x = 800, y = 80)

    window.mainloop()


matplotlib.use("TkAgg")
window = tk.Tk()

length = 1.0
time_end = 1.0
h = 0.01
tau = 0.025
a = 1.0
xnsteps = int(length / h)
tmsteps = int(time_end / tau)
xCoord = [i*h for i in range(xnsteps)]
tCoord = [j*tau for j in range(tmsteps)]

step = 0

Names = ["length", "time_end", "h", "tau", "a", "xnsteps", "tmsteps"]

TotalTemp = [0] * tmsteps
for j in range(tmsteps):
    TotalTemp[j] = [0] * xnsteps

main()