import numpy as np
import matplotlib.pyplot as plt

def InitialConditions(func_x, length):
    return 1/np.sqrt(2 * length) + 1/np.sqrt(length) * np.cos(2 * np.pi * func_x / length)

def Bfunc(func_x, length):
    return 1/np.sqrt(2 * length) + 1/np.sqrt(length) * np.cos(2 * np.pi * func_x / length)

def TridiagonalAlgorithm(a, b, c, d):
    size = len(d)
    alpha = [1] * (size - 1)
    beta = [1] * (size - 1)
    x = [1] * size
    alpha[0] = -c[0] / b[0]
    beta[0] = d[0] / b[0]

    for i in range(1, size - 1):
        alpha[i] = -c[i] / (a[i] * alpha[i-1] + b[i])
        beta[i] = (d[i] - a[i] * beta[i-1]) / (a[i] * alpha[i-1] + b[i])

    x[size-1] = (d[size-1] - a[size-1] * beta[size-2]) / (b[size-1] + a[size-1] * alpha[size-2])

    for i in range(size-2, -1, -1):
        x[i] = alpha[i] * x[i+1] + beta[i]

    return x

def SimpsonMethod(TotalTemp, step, length, xnsteps, h, xCoord):
    Sum = TotalTemp[step][0] * Bfunc(xCoord[0], length) + TotalTemp[step][xnsteps-1] * Bfunc(xCoord[xnsteps-1], length)
    for j in range(1, xnsteps):
        if (j % 2 == 1):
            Sum += 4 * TotalTemp[step][j] * Bfunc(xCoord[j], length)
        else:
            Sum += 2 * TotalTemp[step][j] * Bfunc(xCoord[j], length)
    Sum *= h / 3
    return Sum



def ImplicitMethod(step, TotalTemp, length, time_end, h, tau, a, xnsteps, tmsteps, xCoord, tCoord):
    A = [0] * xnsteps
    B = [0] * xnsteps
    C = [0] * xnsteps
    D = [0] * xnsteps

    factor = a * tau / h**2
    for j in range(1, step + 2):
        D = TotalTemp[j-1]
        Sum = SimpsonMethod(TotalTemp, j-1, length, xnsteps, h, xCoord)
        for i in range(xnsteps):
            A[i] = - factor
            B[i] = 1 + 2 * factor - tau * Bfunc(xCoord[i], length) * TotalTemp[j-1][i] + TotalTemp[j-1][i] * Sum
            C[i] = - factor
        A[0] = 0
        B[0] = 1 + factor - tau * Bfunc(xCoord[0], length) * TotalTemp[j-1][0] + TotalTemp[j-1][0] * Sum
        C[0] = -factor
        A[xnsteps - 1] = -factor
        B[xnsteps - 1] = 1 + factor - tau * Bfunc(xCoord[xnsteps - 1], length) * TotalTemp[j-1][xnsteps-1] + TotalTemp[j-1][xnsteps-1] * Sum
        C[xnsteps - 1] = 0

        TotalTemp[j] = TridiagonalAlgorithm(A, B, C, D)
        # Нормировка (чтобы все было в порядке, а то она уходит куда-то)
        Sum = SimpsonMethod(TotalTemp, j, length, xnsteps, h, xCoord)
        for i in range(xnsteps):
            TotalTemp[j][i] = TotalTemp[j][i] / Sum

    return TotalTemp