import numpy as np
from functions import objective, objective_high_nonlinear
from plotting import plot_doe_results_3d

if __name__ == "__main__":

    smooth_function = False
    x_vals = np.linspace(-5, 10, 30)
    y_vals = np.linspace(-10, 10, 30)

    best_x = None
    best_val = float("inf")
    for x in x_vals:
        for y in y_vals:
            if smooth_function:
                val = objective([x, y])
            else:
                val = objective_high_nonlinear([x, y])
            if val < best_val:
                best_val = val
                best_x = [x, y]

    print("DOE (grid search) result:")
    print("x =", best_x)
    print("f(x) =", best_val)

    # Plotting the results
    if smooth_function:
        plot_doe_results_3d(x_vals, y_vals, best_x, objective)
    else:
        plot_doe_results_3d(x_vals, y_vals, best_x, objective_high_nonlinear)
