import numpy as np
import matplotlib.pyplot as plt

# Задаємо параметри прямої
k_true = 2
b_true = 5

# Генеруємо випадкові дані навколо прямої
n_points = 100
x = np.linspace(0, 10, n_points)
y_true = k_true * x + b_true
y = y_true + np.random.normal(scale=2, size=n_points)  # Додаємо шум

# Функція для обчислення градієнту
def compute_gradient(x, y, k, b):
    y_pred = k * x + b
    grad_k = -2 * np.mean(x * (y - y_pred))
    grad_b = -2 * np.mean(y - y_pred)
    return grad_k, grad_b

# Функція для градієнтного спуску
def gradient_descent(x, y, learning_rate, n_iter):
    k = 0  # Початкова оцінка для k
    b = 0  # Початкова оцінка для b
    for _ in range(n_iter):
        grad_k, grad_b = compute_gradient(x, y, k, b)
        k -= learning_rate * grad_k
        b -= learning_rate * grad_b
    return k, b

# Параметри градієнтного спуску
learning_rate = 0.01
n_iter = 1000

# Отримуємо оптимальні оцінки kk та bb за допомогою градієнтного спуску
k_gd, b_gd = gradient_descent(x, y, learning_rate, n_iter)

# Вивід результатів
print("Оцінка методом градієнтного спуску:")
print("k_gd:", k_gd)
print("b_gd:", b_gd)

# Графік
plt.figure(figsize=(10, 6))
plt.scatter(x, y, label='Дані з шумом')
plt.plot(x, y_true, color='red', linestyle='--', label='Початкова пряма')
plt.plot(x, k_gd * x + b_gd, color='orange', label='Оцінка методом градієнтного спуску')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Оцінка лінії регресії методом градієнтного спуску')
plt.legend()
plt.grid(True)
plt.show()

# Графік похибки від кількості ітерацій
errors = []
for i in range(1, n_iter + 1):
    k_gd, b_gd = gradient_descent(x, y, learning_rate, i)
    y_pred = k_gd * x + b_gd
    error = np.mean((y - y_pred) ** 2)
    errors.append(error)

plt.figure(figsize=(10, 6))
plt.plot(range(1, n_iter + 1), errors, color='blue')
plt.xlabel('Кількість ітерацій')
plt.ylabel('Похибка')
plt.title('Графік похибки від кількості ітерацій')
plt.grid(True)
plt.show()
