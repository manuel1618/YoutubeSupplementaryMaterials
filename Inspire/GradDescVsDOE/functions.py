import numpy as np


def objective_high_nonlinear(x):
    return (x[0] - 3) ** 2 + (x[1] + 1) ** 2 + 9 * np.sin(x[0]) * 7 * np.cos(x[1])


def gradient_high_nonlinear(x):
    dx = 2 * (x[0] - 3) + np.cos(x[0]) * np.cos(x[1])
    dy = 2 * (x[1] + 1) - np.sin(x[0]) * np.sin(x[1])
    return np.array([dx, dy])


# Objective function
def objective(x):
    return (x[0] - 3) ** 2 + (x[1] + 1) ** 2


# Gradient of the objective
def gradient(x):
    dx = 2 * (x[0] - 3)
    dy = 2 * (x[1] + 1)
    return np.array([dx, dy])
