import numpy as np # Для створення нульової матриці
from tabulate import tabulate # Для виводу розподілу у таблиці
from scipy.optimize import linprog # Для розв'язку за допомогою бібліотеки

# Виведення таблиці з відступом за допомогою символу табуляції
def output_table_allocation(allocation, count_tab=2):
    table_str = tabulate(allocation, tablefmt="grid")
    indented_table_str = "\n".join(("\t" * abs(count_tab)) + line for line in table_str.split("\n"))
    return indented_table_str

# Реалізація методу північно-західного кута
def northwest_corner_method(costs, supplies, demands):
    rows, cols = len(supplies), len(demands)
    allocation = np.zeros((rows, cols))
    min_cost = 0

    print("=" * 50)

    # Перевірка на валідність вхідних даних
    if np.sum(supplies) != np.sum(demands):
        raise ValueError("Сума постачань має бути рівною сумі вимог")

    # Вираховуємо розмір постачання/попиту за методом північно-західного кута
    i, j, counter = 0, 0, 1
    while i < rows and j < cols:
        # Обчислюємо кількість, яку можемо перенести
        quantity = min(supplies[i], demands[j])
        # Виділяємо цю кількість товару
        allocation[i][j] = quantity
        # Зменшуємо доступні поставки та попит
        supplies[i] -= quantity
        demands[j] -= quantity
        # Обраховуємо значення мінімальної вартості
        min_cost += costs[i][j] * quantity
        # Виводимо кожну ітерацію
        print(f"Ітерація № {i+1}.{j+1} (загальна кількість {counter}):")
        print(f"\tРозподіл у таблиці:")
        print(output_table_allocation(allocation))
        print(f"\t\tЗапаси, що залишились: {supplies}")
        print(f"\t\tПотреби, що залишились: {demands}")
        print("=" * 50)

        # Якщо запаси вичерпані, переходимо до наступного рядка
        if supplies[i] == 0:
            i += 1
        # Якщо потреби вичерпано, переходимо до наступного стовпця
        if demands[j] == 0:
            j += 1

        counter += 1

    return allocation, min_cost

# Значення розв'язане за допомогою бібліотеки Python
def solve_transportation_problem_with_library(costs, supplies, demands):
    #  Перевірка на валідність вхідних даних
    if np.sum(supplies) != np.sum(demands):
        raise ValueError("Сума постачань має бути рівною сумі вимог")

    # Побудова матриці розподілу
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
    list_res = res.x.reshape((num_suppliers, num_customers))

    # Вивід результатів
    print("\tОптимальний план перевезень:")
    print(output_table_allocation(list_res))
    print("\tМінімальне значення цільової функції:", res.fun)

if __name__ == '__main__':
    print("Програму створив Павло Вальчевський, група ОІ-11сп, ЛР № 4, варіант № 91, Дослідження операцій (ММДО або ДО)")

    # Дані для варіанту № 91
    costs = np.array([[1, 3, 3, 8],
                      [8, 6, 2, 6],
                      [7, 7, 3, 8],
                      [5, 2, 4, 5]])
    supplies = np.array([20, 20, 40, 45])
    demands = np.array([25, 30, 40, 30])

    # Вивід рузультатів методу північно-західного кута
    print("Початок розрахунку!")
    print("Розв'язок знайдений через метод північно-західного кута з виводом ітерацій:")
    allocation, min_cost = northwest_corner_method(costs.copy(), supplies.copy(), demands.copy())
    print("\tОптимальний план перевезень:")
    print(output_table_allocation(allocation, 2))
    print(f"\tЗначення мінімальних витрат: {min_cost}")
    print("=" * 50)
    # Вивід рузультатів через бібліотеку Пайтон
    print("Розв'язок знайдений через бібліотеку Пайтон (без ітерацій):")
    solve_transportation_problem_with_library(costs.copy(), supplies.copy(), demands.copy())
    print("=" * 50)
    print("Програму завершено!")