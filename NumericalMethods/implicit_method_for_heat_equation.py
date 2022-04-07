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

def tridiagonal_alg(n, A, B, C, G):
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

    T_1 = tridiagonal_alg(n-3, A, B, C, F)
    T_1.insert(0, 0)
    T_1.append(0)

    return T_0, T_1

def test():
    a, l, n, _T_, m = 1.0, 1.0, 6, 1.0, 30
    data = [l, n, _T_, m]
    h, tau = calc(data)

    x = [i*h for i in range(n)]
    t = [j*tau for j in range(m)]

    T_0 = [f2(_x, 0) for _x in x]
    T_0[0] = 0
    T_0[-1] = 0

    for j in range(m-1):
        F = [f(_x, t[j+1]) for _x in x]

        lam = a**2 * tau / h**2

        A = [-lam for i in range(n-2)]
        B = [1 + 2 *lam for i in range(n-2)]
        C = [-lam for i in range(n-2)]
        D = [T_0[i+1] + tau * F[i+1] for i in range(n-2)]

        # !
        print(A)
        print(B)
        print(C)
        print(D)

        T_1 = tridiagonal_alg(n-3, A, B, C, D)
        T_1.insert(0, T_0[0])
        T_1.append(T_0[-1])

        # !
        print(T_1)

        plt.plot(x, T_0, color="blue")
        plt.plot(x, T_1, color="red")
        plt.show()

        T_0 = T_1

if __name__ == "__main__":
    test()
