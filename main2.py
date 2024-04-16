import numpy as np

class TransportationProblemSolver:
    def __init__(self, costs, supplies, demands):
        self.costs = costs
        self.supplies = supplies
        self.demands = demands
        self.num_suppliers = len(supplies)
        self.num_customers = len(demands)
        self.num_variables = self.num_suppliers * self.num_customers

    def solve(self):
        # Ініціалізація проміжних змінних
        allocation = np.zeros((self.num_suppliers, self.num_customers))
        u = np.zeros(self.num_suppliers)
        v = np.zeros(self.num_customers)
        num_allocated = 0

        while num_allocated < self.num_variables:
            # Розрахунок потенціалів
            for i in range(self.num_suppliers):
                for j in range(self.num_customers):
                    if allocation[i][j] != 0:
                        continue
                    elif u[i] == 0 and v[j] == 0:
                        continue
                    elif u[i] == 0:
                        u[i] = self.costs[i][j] - v[j]
                    elif v[j] == 0:
                        v[j] = self.costs[i][j] - u[i]

            # Пошук мінімального потенціалу
            min_potential = np.inf
            min_i = min_j = None
            for i in range(self.num_suppliers):
                for j in range(self.num_customers):
                    if allocation[i][j] == 0:
                        potential = u[i] + v[j] - self.costs[i][j]
                        if potential < min_potential:
                            min_potential = potential
                            min_i, min_j = i, j

            allocation[min_i][min_j] = min(self.supplies[min_i], self.demands[min_j])
            self.supplies[min_i] -= allocation[min_i][min_j]
            self.demands[min_j] -= allocation[min_i][min_j]
            num_allocated += 1

            # Вивід проміжних результатів
            print(f"Проміжний план {num_allocated}:")
            print(allocation)




        # Розрахунок значення цільової функції
        total_cost = np.sum(allocation * self.costs)
        print("\nОптимальний план перевезень:")
        print(allocation)
        print("Мінімальне значення цільової функції:", total_cost)

# Дані
costs = np.array([[1, 3, 3, 8],
                  [8, 6, 2, 6],
                  [7, 7, 3, 8],
                  [5, 2, 4, 5]])
supplies = np.array([20, 20, 40, 45])
demands = np.array([25, 30, 40, 30])

print("Програму створив Павло Вальчевський, група ОІ-11сп, ЛР № 4, Дослідження операцій (ММДО або ДО)")

# Розв'язання
solver = TransportationProblemSolver(costs, supplies, demands)
solver.solve()
print("Програма у цьому коді має виводити ітерації, але вона недокінця добре розроблена (написав аналог на С++)")