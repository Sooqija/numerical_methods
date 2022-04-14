import numpy as np
import matplotlib.pyplot as plt

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


def f(x, t):
    return 1 + np.cos(np.pi * x)


def f1(x, t):
    return np.sin(x)*t + np.sin(x)


def f2(x, t):
    return 1 + np.cos(2*np.pi*x)


def f3(x, t):
    return sin(3 * pi * x / 2)


def f4(x, t):
    return 4.0 * (1.0 - x) * x

def f5(x, t):
    return 4.0 * (1.0 - x) * t + x * t


def my_tridiagonal_alg(a, b, f):
    n = len(a)
    alpha = np.zeros(n)
    beta = np.zeros(n)
    y = np.zeros(n)
    x = np.zeros(n)
    if n:
        alpha[0] = (np.sqrt(a[0]))
        for i in range(1, n):
            beta[i-1] = b[i-1] / alpha[i-1]
            alpha[i] = a[i] - (beta[i-1])**2
        beta[n-1] = b[n-1] / alpha[n-1]
        y[0] = f[0] / alpha[0]
        for i in range(1, n):
            y[i] = (f[i] - beta[i-1] * y[i-1]) / (alpha[i])
        x[n-1] = y[n-1] / alpha[n-1]
        for i in range(n-2, -1, -1):
            x[i] = (y[i] - beta[i] * x[i+1]) / (alpha[i])

    return list(x)


def solve(h, tau, a, n, m, l, _T_, time, T_0=[]):
    x = [i*h for i in range(n)]
    T_const = 0
    if not (len(T_0)):
        T_0 = [f2(_x, time) for _x in x]
        T_0[0] = T_const
        T_0[-1] = T_const
    F = [f(_x, time) for _x in x]

    lam = a**2 * tau / h**2

    _a_ = [1 + 2 *lam for i in range(n-2)]
    _b_ = [-lam for i in range(n-2)]
    _F_ = [T_0[i+1] + tau * F[i+1] for i in range(n-2)]

    T_1 = my_tridiagonal_alg(_a_, _b_, _F_)
    T_1.insert(0, T_const)
    T_1.append(T_const)

    return T_0, T_1

def test():
    a, l, n, _T_, m = 1.0, 1.0, 6, 1.0, 30
    data = [l, n, _T_, m]
    h, tau = calc(data)

    x = [i*h for i in range(n)]
    t = [j*tau for j in range(m)]

    T_const = 0
    T_0 = [f2(_x, 0) for _x in x]
    T_0[0] = T_const
    T_0[-1] = T_const

    for j in range(m-1):
        F = [f(_x, t[j+1]) for _x in x]

        lam = a**2 * tau / h**2

        _a_ = [1 + 2 *lam for i in range(n-2)]
        _b_ = [-lam for i in range(n-2)]
        _F_ = [T_0[i+1] + tau * F[i+1] for i in range(n-2)]

        T_1 = my_tridiagonal_alg(_a_, _b_, _F_)
        T_1.insert(0, T_const)
        T_1.append(T_const)

        plt.plot(x, T_0, color="blue")
        plt.plot(x, T_1, color="red")
        plt.show()

        T_0 = T_1

if __name__ == "__main__":
    test()
