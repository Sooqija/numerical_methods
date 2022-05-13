import numpy as np
import matplotlib.pyplot as plt
def InitialCondition(func_x):
    return phi_a + phi_b * np.cos(np.pi * func_x / length) + phi_c * np.cos(2 * np.pi * func_x / length)

def BFunction(func_x):
    return 1/length +  np.cos(np.pi * func_x / length) + 0 * np.cos(2 * np.pi * func_x / length)

def simp(i):
    if (i % 2 == 0):
        return 2
    else:
        return 4

def SimpsonMethod(time):
    x = h
    res = BFunction(0) * Temp[time][0]
    for i in range(1, xNumSteps - 1):
        res += BFunction(x) * simp(i) * Temp[time][i]
        x += h
    res += BFunction(x) * Temp[time][xNumSteps - 1]
    return res * (h / 3)

def ExplicitMethod():
    for j in range(1, tNumSteps):
        Temp[j-1].insert(0, Temp[j-1][0])
        Temp[j-1].append(Temp[j-1][-1])
        if tau > h**2 / 2:
            print("Условия устойчивости шаблона явной схемы не выполнены: tau > h**2 / 2")
            Temp[j-1].pop()
            Temp[j-1].pop(0)
            break
        for i in range(xNumSteps):
            Temp[j][i] = Temp[j-1][i+1] + tau * (Temp[j-1][i+2] - 2*Temp[j-1][i+1] + Temp[j-1][i]/ h**2 + Temp[j-1][i] * h * h * ((tau * (BFunction(x) - SimpsonMethod(j-1))) + 1))
        Temp[j-1].pop()
        Temp[j-1].pop(0)
        # for i in range(1, -1, -1):
        #     if i < xNumSteps-1:
        #         Temp[j][i] = Temp[j][i+1]
        #         Temp[j][-(i+1)] = Temp[j][-(i+2)]

def SolveTridiagonal(downDiagonal, midDiagonal, upDiagonal, d, j):
    size = len(midDiagonal)
    if (size == len(downDiagonal) + 1 and size == len(upDiagonal) + 1 and size == len(d)):
        alpha = [0] * (size - 1)
        beta = [0] * (size - 1)
        alpha[0] = -upDiagonal[0] / midDiagonal[0]
        beta[0] = -d[0] / midDiagonal[0]

        for i in range(size - 1):
            gamma = midDiagonal[i] + downDiagonal[i-1] * alpha[i-1]
            alpha[i] = -upDiagonal[i] / gamma
            beta[i] = (d[i] -upDiagonal[i-1] * beta[i-1]) / gamma

        Temp[j][size-1] = (d[size-1] - downDiagonal[size-2]*beta[size-2]) / (midDiagonal[size-1] + downDiagonal[size-2]*alpha[size-2])

        for i in range(size - 2, -1, -1):
            Temp[j][i] = alpha[i]*Temp[j][i+1] + beta[i]

def ImplicitMethod():
    upDiagonal = [0] * (xNumSteps - 1)
    midDiagonal = [0] * (xNumSteps)
    downDiagonal = [0] * (xNumSteps - 1)
    factor = a**2 * tau / h**2
    for i in range(xNumSteps-1):
        if (i == 0):
            upDiagonal[i] = -2 * factor
        else:
            upDiagonal[i] = -1 * factor
    for i in range(xNumSteps):
        midDiagonal[i] = h * h + 2*factor
    for i in range(xNumSteps-1):
        if (i == xNumSteps - 2):
            upDiagonal[i] = -2 * factor
        else:
            upDiagonal[i] = -1 * factor

    for j in range(1, tNumSteps):
        x = 0
        d = [0] * xNumSteps
        simpson = SimpsonMethod(j-1)
        for i in range(xNumSteps):
            d[i] = Temp[j-1][i] * h * h * ((tau * (BFunction(x) - simpson)) + 1)
            x += h
        SolveTridiagonal(downDiagonal, midDiagonal, upDiagonal, d, j)

a = 1.0
T_end = 1.0
length = 7.0
tau = 0.1
h = 0.1

phi_a = 1 / length
phi_b = 1
phi_c = 2

b_a = 0
b_b = 0.3
b_c = 0

xNumSteps = int(length / h + 1)
tNumSteps = int(T_end / tau + 1)

Temp = [0] * tNumSteps
for j in range(tNumSteps):
    Temp[j] = [0] * xNumSteps

x = 0
for i in range(xNumSteps):
    Temp[0][i] = InitialCondition(x)
    x += h


coord_x = [i*h for i in range(xNumSteps)]
for j in range(0, tNumSteps):
    ExplicitMethod()
    plt.plot(coord_x, Temp[j])
    ImplicitMethod()
    plt.plot(coord_x, Temp[j])
    plt.show()

