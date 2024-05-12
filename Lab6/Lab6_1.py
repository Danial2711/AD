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

# Функція для методу найменших квадратів
def least_squares(x, y):
    X = np.vstack([x, np.ones(len(x))]).T
    return np.linalg.inv(X.T @ X) @ X.T @ y

# Знаходимо оцінки kk та bb за допомогою методу найменших квадратів
k_est, b_est = least_squares(x, y)

# Оцінка параметрів прямої за допомогою np.polyfit
k_polyfit, b_polyfit = np.polyfit(x, y, 1)

# Вивід результатів
print("Оцінка методом найменших квадратів:")
print("k_est:", k_est)
print("b_est:", b_est)
print()
print("Оцінка за допомогою np.polyfit:")
print("k_polyfit:", k_polyfit)
print("b_polyfit:", b_polyfit)
print()
print("Початкові параметри прямої:")
print("k_true:", k_true)
print("b_true:", b_true)

# Графік
plt.figure(figsize=(10, 6))
plt.scatter(x, y, label='Дані з шумом')
plt.plot(x, y_true, color='red', linestyle='--', label='Початкова пряма')
plt.plot(x, k_est * x + b_est, color='green', label='Оцінка методом найменших квадратів')
plt.plot(x, k_polyfit * x + b_polyfit, color='blue', label='Оцінка за допомогою np.polyfit')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Оцінка лінії регресії')
plt.legend()
plt.grid(True)
plt.show()
