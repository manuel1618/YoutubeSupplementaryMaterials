
# 🔧 Optimization Comparison: Gradient-Based vs DOE

We compare two optimization approaches on a simple convex problem:

## 🧠 Problem Definition

Objective function:
$f(x, y) = (x - 3)^2 + (y + 1)^2$

This function has a global minimum at **(x, y) = (3, -1)** with **f(x, y) = 0**.

---

## 1️⃣ Design of Experiments (DOE) – Grid Search

```python
import numpy as np

# Objective function
def objective(x):
    return (x[0] - 3)**2 + (x[1] + 1)**2

# Define DOE grid
x_vals = np.linspace(-5, 10, 100)
y_vals = np.linspace(-10, 10, 100)

# Evaluate all points
best_x = None
best_val = float('inf')

for x in x_vals:
    for y in y_vals:
        val = objective([x, y])
        if val < best_val:
            best_val = val
            best_x = [x, y]

print("DOE (grid search) result:")
print("x =", best_x)
print("f(x) =", best_val)
```

---

## 2️⃣ Gradient-Based Optimization (Gradient Descent from Scratch)

```python
import numpy as np

# Objective function
def objective(x):
    return (x[0] - 3)**2 + (x[1] + 1)**2

# Gradient of the objective
def gradient(x):
    dx = 2 * (x[0] - 3)
    dy = 2 * (x[1] + 1)
    return np.array([dx, dy])

# Gradient descent
def gradient_descent(starting_point, learning_rate=0.1, max_iters=100, tolerance=1e-6):
    x = np.array(starting_point, dtype=float)
    for i in range(max_iters):
        grad = gradient(x)
        x_new = x - learning_rate * grad
        if np.linalg.norm(x_new - x) < tolerance:
            break
        x = x_new
    return x, objective(x)

# Run gradient descent
start = [0, 0]
opt_x, opt_val = gradient_descent(start)

print("Gradient Descent Result:")
print("x =", opt_x)
print("f(x) =", opt_val)
```

---

## ✅ Summary

| Method           | Result (x, y)      | f(x, y)        | Notes                                 |
|------------------|--------------------|----------------|---------------------------------------|
| DOE (Grid Search)| ~[3, -1] (approx)  | ~0 (grid limit)| Simple, exhaustive, but slow          |
| Gradient Descent | [3.0, -1.0]        | 0.0            | Fast and accurate for smooth problems |

---
