import numpy as np
from functions import (
    gradient,
    gradient_high_nonlinear,
    objective,
    objective_high_nonlinear,
)
from plotting import plot_descent_path, plot_descent_path_3d


# Gradient descent
def gradient_descent(
    starting_point, gradient, learning_rate=0.2, max_iters=1000, tolerance=1e-6
):
    point = np.array(starting_point, dtype=float)
    path = [point]
    for i in range(max_iters):
        grad = gradient(point)
        x_new = point - learning_rate * grad
        path.append(x_new)
        if np.linalg.norm(x_new - point) < tolerance:
            break
        point = x_new
    return path


if __name__ == "__main__":
    smooth_function = False
    start = [0, 0]
    if smooth_function:
        # Run gradient descent - smooth function
        path = gradient_descent(start, gradient)
        print("Gradient Descent Result:")
        print("x =", path[-1])
        print("f(x) =", objective(path[-1]))
        # plot_descent_path(start, path, objective)
        plot_descent_path_3d(start, path, objective)
    else:
        # Run gradient descent - non-smooth function
        path = gradient_descent(start, gradient_high_nonlinear)
        print("Gradient Descent Result:")
        print("x =", path[-1])
        print("f(x) =", objective_high_nonlinear(path[-1]))
        # plot_descent_path(start, path, objective_high_nonlinear)
        plot_descent_path_3d(start, path, objective_high_nonlinear)
