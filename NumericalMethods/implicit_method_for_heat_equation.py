from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import math
from math import sin, cos, pi

'''
    ## Take a short look at the heat equation

    The общий вид уравнения

    u' = a**2 u''_xx_ + f(x, t)

    a - diffusitivity of the rod, теплопроводность стержня

    x - coordinate on the rod
    T - temperature of part of the rod at point x
    t - временные отрезки, на которых изменяется температура стержня на всех его участках

    h - шаг сетки по x
    tau - шаг сетки по t
    l - длина стержня
    n - кол-во шагов h, тогда логично, что l = n*h
    _T_ - конечное время нагрева стержня
    m - количество шагов tau, тогда логично, что _T_ = tau*m

    При этом:
    1. x = (0, l)
    2. tau = (0, _T_)

    сетка - это координатная плоскость, на которой по оси x откладываются собственно координаты x, а по оси y координаты времени. При этом, каждая точка соответственно владеет 3-ей координатой, которую и предстоит аппроксимировать - температурой.

    Важные условия:
    1. Концы стержня теплоизолированы, изменение их температуры равно 0, т.е.
        u'_x_(0, t) = 0
        u'_x_(l, t) = 0
    2. Начальное распределение температуры по стержню определяется функцией
        u(x, 0) = phi(x)

        Функция f(x, t) выбирается в виде
            f(x, t) = b(x) * u(x, t)
        1/l + lambda*cos(pi * x / l)
'''

def calc(data): # data = [l, n, _T_, m]
    h = data[0] / data[1]
    tau = data[2] / data[3]
    return h, tau

def f(x, t): # now it's phi
    return 1 + cos(pi * x)

def f1(x, t):
    return np.sin(x)*t + np.sin(x)

def f2(x, t):
    return 1 + np.cos(2*pi*x)

def f3(x, t):
    return sin(3 * pi * x / 2)

def f4(x, t): # now it's u(x, 0)
    return 4.0 * (1.0 - x) * x

def f5(x, t):
    return 5

def run_matrix(n, A, B, C, G):
    s = np.zeros(n + 1)
    t = np.zeros(n + 1)
    y = np.zeros(n + 1)
    s[0] = C[0] / B[0]
    t[0] = -G[0] / B[0]
    for i in range(1, n + 1):
        s[i] = C[i] / (B[i] - A[i] * s[i-1])
        t[i] = (A[i] * t[i-1] - G[i]) / (B[i] - A[i]*s[i-1])
    y[n] = t[n]
    for i in range(n-1, -1, -1):
        y[i] = s[i] * y[i+1] + t[i]
    return list(y)

def solve(h, tau, a, n, m, l, _T_, time, T_0=[]):
    x = [i*h for i in range(n)]
    if not (len(T_0)):
        T_0 = [f2(_x, time) for _x in x]
        T_0[0] = 0
        T_0[-1] = 0
    _F_ = [f(_x, time) for _x in x]

    lam = a**2 * tau / h**2

    A = [-lam for i in range(n-2)]
    B = [1 + 2 *lam for i in range(n-2)]
    C = [-lam for i in range(n-2)]
    F = [T_0[i+1] + tau * _F_[i+1] for i in range(n-2)]

    # A = [1 for i in range(n-2)]
    # B = [-(h**2 / (tau * a**2) + 2) for i in range(n-2)]
    # C = [1 for i in range(n-2)]
    # F = [(-(h**2)/(a**2)) * (_F_[i+1] + T_0[i+1]/tau) for i in range(n-2)]

    T_1 = run_matrix(n-3, A, B, C, F)
    T_1.insert(0, 0)
    T_1.append(0)

    return T_0, T_1

if __name__ == "__main__":
    h, tau, a, n, m, l, _T_ = get_coef() # ???

    t = [j*tau for j in range(m)]
    x_0 = [i*h for i in range(n)]
    T_0 = [f2(x, 0) for x in x_0]
    T_begin = 0
    # T_0[0] = T_begin
    # T_0[n-1] = T_begin
    T_1 = [None for j in range(m)]

    for j in range(m):
        _F_ = [f(x, t[j]) for x in x_0]

        A = [1 for i in range(n-2)]
        B = [-(h**2 / (tau * a**2) + 2) for i in range(n-2)]
        print(B)
        C = [1 for i in range(n-2)]
        F = [(-(h**2)/(a**2)) * (_F_[i+1] + T_0[i+1]/tau) for i in range(n-2)]
        print(F)
        T_1 = run_matrix(n-3, A, B, C, F)
        print(T_1)
        T_1.insert(0, T_0[0])
        T_1.append(T_0[-1])


        plt.plot(x_0, list(map(abs, T_0)), color="green")
        plt.plot(x_0, list(map(abs, T_1)), color="red")
        plt.show()

        T_0 = T_1


    # plt.plot(x_0, list(map(abs, T_0)), color="green")
    # plt.plot(x_0, list(map(abs, T_1)), color="red")
    # plt.show()

    # T_0 = T_1
# def tridiagonal_alg(A, C, B, F):
#     n = len(F)
#     alf = [0 for i in range(n)]
#     bet = [0 for i in range(n)]
#     X = [0 for i in range(n)]
#     alf[1], bet[1] = -B[0]/C[0], F[0]/C[0]
#     for i in range(2, n):
#         alf[i] = -B[i-1]/(A[i-1]*alf[i-1] + C[i-1])
#         bet[i] = (F[i-1] - A[i-1]*bet[i-1])/(A[i-1]*alf[i-1] + C[i-1])
#     X[n-1] = (F[n-1] - A[n-1]*bet[n-1])/(A[n-1]*alf[n-1] + C[n-1])
#     for i in reversed(range(n-1)):
#         # print i
#         X[i] = alf[i+1]*X[i+1] + bet[i+1]
#     # print alf
#     # print bet
#     return X


# X1, T1 = np.mgrid[0:15:10j, 0:5:10j]
# Z_sol = U(X1, T1)
# F_res = f(X1, T1)
# # print(Z_sol[10,:])





# X = [i*h for i in range(n)]
# T = [i*tau for i in range(n)]
# U_res = [[0 for i in range(n)] for j in range(n)]
# U_res2 = [[0 for i in range(n)] for j in range(n)]
# # F_res = [[f(X[j], T[i]) for j in range(n)] for i in range(n)]

# for i in range(n):
#     U_res[i][0] = phi(X[i])
#     U_res[0][i] = psi0(T[i])
#     U_res[n-1][i] = psil(T[i])

# for i in range(n):
#     for j in range(n):
#         U_res2[i][j] = U(X[i], T[j])

# A = [1 for i in range(n-2)]
# B = [-(2 + h**2/tau/a**2) for i in range(n-2)]
# C = [1 for i in range(n-2)]

# for i in range(1, n):
#     F = [-(F_res[j][i] + U_res[j][i-1]/tau)*(h**2)/(a**2) for j in range(1, n-1)]
#     F[0] -= U_res[0][i]
#     F[n-3] -= U_res[n-1][i]
#     temp = tridiagonal_alg(A, B, C, F)
#     for j in range(1, n-1):
#         U_res[j][i] = temp[j-1]

# plt.figure(figsize=(10.,5.))
# plt.xlabel("r")
# plt.ylabel(f"$\Lambda$")


# print(len(X1))
# print(X1)
# print(T1)
# plt.plot(X1, T1[9], color='black')

# plt.show()


# fig = plt.figure()
# ax = fig.gca(projection='3d')
# # ax.plot_surface(X1, T1, U_res, rstride=8, cstride=8, alpha=0.3, color='green')
# ax.plot_surface(X1, T1, Z_sol, rstride=8, cstride=8, alpha=0.3, color='red')

# ax.set_xlabel('X')
# ax.set_xlim(0*h, 15)
# ax.set_ylabel('T')
# ax.set_ylim(0, 5)
# ax.set_zlabel('U')
# ax.set_zlim(-7, 7)

# plt.show()