import numpy as np
from scipy.optimize import linprog

def solve_transportation_problem(costs, supplies, demands):
    # Перевірка на валідність вхідних даних
    if np.sum(supplies) != np.sum(demands):
        raise ValueError("Сума постачань має бути рівною сумі вимог")

    # Побудова матриці вартостей перевезень
    num_suppliers = len(supplies)
    num_customers = len(demands)
    num_variables = num_suppliers * num_customers
    c = costs.flatten()

    # Побудова обмежень
    A_eq = np.zeros((num_suppliers + num_customers, num_variables))
    b_eq = np.zeros(num_suppliers + num_customers)

    for i in range(num_suppliers):
        A_eq[i, i*num_customers:(i+1)*num_customers] = 1
        b_eq[i] = supplies[i]

    for j in range(num_customers):
        A_eq[num_suppliers + j, j::num_customers] = 1
        b_eq[num_suppliers + j] = demands[j]

    # Виклик лінійного програмування для пошуку оптимального рішення
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, method='highs')

    # Вивід результатів
    print("Оптимальний план перевезень:")
    print(res.x.reshape((num_suppliers, num_customers)))
    print("Мінімальне значення цільової функції:", res.fun)

# Дані
costs = np.array([[1, 3, 3, 8],
                  [8, 6, 2, 6],
                  [7, 7, 3, 8],
                  [5, 2, 4, 5]])
supplies = np.array([20, 20, 40, 45])
demands = np.array([25, 30, 40, 30])

print("Програму створив Павло Вальчевський, група ОІ-11сп, ЛР № 4, Дослідження операцій (ММДО або ДО)")

# Розв'язання
solve_transportation_problem(costs, supplies, demands)
