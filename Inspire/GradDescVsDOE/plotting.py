import matplotlib.pyplot as plt
import numpy as np
from functions import objective, objective_high_nonlinear


# plot the objective function
def plot_objective_function_color_map(x_vals, y_vals, objective_func):

    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.array([[objective_func([x, y]) for x in x_vals] for y in y_vals])

    plt.figure(figsize=(10, 6))
    plt.contourf(X, Y, Z, levels=50, cmap="viridis")
    plt.colorbar(label="Objective Function Value")
    plt.title("Objective Function Contour Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()


def plot_objective_function_3d(x_vals, y_vals, objective_func):
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.array([[objective_func([x, y]) for x in x_vals] for y in y_vals])

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
    ax.set_title("Objective Function 3D Surface Plot, Min at (3, -1, 0)")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Objective Function Value")
    # mark the mininum point and label it
    min_x = 3
    min_y = -1
    min_z = objective_func([min_x, min_y])
    ax.scatter(min_x, min_y, min_z, color="red", s=100, label="Minimum Point")
    ax.legend()
    plt.show()


def plot_descent_path(start, path, objective_func):
    x_vals = np.linspace(-5, 10, 30)
    y_vals = np.linspace(-10, 10, 30)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.array([[objective_func([x, y]) for x in x_vals] for y in y_vals])

    plt.figure(figsize=(10, 6))
    plt.contourf(X, Y, Z, levels=50, cmap="viridis")
    plt.colorbar(label="Objective Function Value")

    # Plot the gradient descent path
    path = np.array(path)
    plt.plot(
        path[:, 0], path[:, 1], marker="o", color="red", label="Gradient Descent Path"
    )

    plt.title("Gradient Descent Path on Objective Function")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.show()


def plot_descent_path_3d(start, path, objective_func):
    x_vals = np.linspace(-5, 10, 30)
    y_vals = np.linspace(-10, 10, 30)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.array([[objective_func([x, y]) for x in x_vals] for y in y_vals])

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")
    # Plot the objective function surface - make it transparent
    ax.plot_surface(X, Y, Z, alpha=0.5, cmap="viridis", edgecolor="none")
    ax.set_title("Gradient Descent Path on Objective Function")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Objective Function Value")

    # Plot the gradient descent path, make it bigger and red
    path_incluing_z = np.array(
        [np.append(p, objective_func(p)) for p in path], dtype=float
    )
    ax.plot(
        path_incluing_z[:, 0],
        path_incluing_z[:, 1],
        path_incluing_z[:, 2],
        marker="o",
        color="red",
        label="Gradient Descent Path",
    )

    plt.legend()
    plt.show()


def plot_doe_results_3d(x_vals, y_vals, best_x, objective_func):
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.array([[objective_func([x, y]) for x in x_vals] for y in y_vals])

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")
    # Plot the objective function surface - make it transparent
    ax.plot_surface(X, Y, Z, alpha=0.5, cmap="viridis", edgecolor="none")
    ax.set_title("DOE Results on Objective Function")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Objective Function Value")

    # Plot the best DOE point
    ax.scatter(
        best_x[0],
        best_x[1],
        objective_func(best_x),
        marker="o",
        color="red",
        label="Best DOE Point",
    )

    # plot all other points in the grid (greyed out, smaller)
    for x in x_vals:
        for y in y_vals:
            if [x, y] != best_x:
                ax.scatter(
                    x,
                    y,
                    objective_func([x, y]),
                    marker="o",
                    color="grey",
                    s=2,
                    alpha=0.5,
                )

    plt.legend()
    plt.show()

    # save as 3d pdf
    fig.savefig("doe_results.pdf", format="pdf")


def plot_doe_results(x_vals, y_vals, best_x, objective_func):

    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.array([[objective_func([x, y]) for x in x_vals] for y in y_vals])

    plt.figure(figsize=(10, 6))
    plt.contourf(X, Y, Z, levels=50, cmap="viridis")
    plt.colorbar(label="Objective Function Value")

    # Plot the best DOE point
    plt.plot(best_x[0], best_x[1], marker="o", color="red", label="Best DOE Point")

    # plot all other points in the grid (greyed out, smaller)
    for x in x_vals:
        for y in y_vals:
            if [x, y] != best_x:
                plt.plot(x, y, marker="o", color="grey", markersize=2, alpha=0.5)

    plt.title("DOE Results on Objective Function")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Define the grid for DOE
    x_vals = np.linspace(-5, 10, 30)
    y_vals = np.linspace(-10, 10, 30)

    # Plot the objective function
    # plot_objective_function_3d(x_vals, y_vals, objective)
    plot_objective_function_3d(x_vals, y_vals, objective_high_nonlinear)
