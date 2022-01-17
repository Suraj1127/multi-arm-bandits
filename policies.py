import numpy as np


def explore(days):

    # Exploration only
    total_happiness = 0
    optimum_happiness = 0

    total_happiness_a = 0
    total_happiness_b = 0
    total_happiness_c = 0

    a = b = c = 0

    for day in range(1, days + 1):

        happiness_a = np.random.normal(10, 5)

        random_value = np.random.rand()

        if random_value <= 1 / 3:
            total_happiness += happiness_a
            total_happiness_a += happiness_a
            a += 1
        elif random_value <= 2 / 3:
            happiness_b = np.random.normal(8, 4)
            total_happiness += happiness_b
            total_happiness_b += happiness_b
            b += 1
        else:
            happiness_c = np.random.normal(5, 2.5)
            total_happiness += happiness_c
            total_happiness_c += happiness_c
            c += 1

        optimum_happiness += happiness_a

    regret = optimum_happiness - total_happiness
    avg_happiness_arr = [total_happiness_a / a, total_happiness_b / b, total_happiness_c / c]

    return optimum_happiness, total_happiness, regret, avg_happiness_arr


def exploit(days):

    # Exploitation only
    total_happiness = 0
    optimum_happiness = 0

    happiness_a = np.random.normal(10, 5)
    happiness_b = np.random.normal(8, 4)
    happiness_c = np.random.normal(5, 2.5)

    happiness_a_2 = np.random.normal(10, 5)
    happiness_a_3 = np.random.normal(10, 5)

    total_happiness += (happiness_a + happiness_b + happiness_c)
    optimum_happiness += (happiness_a + happiness_a_2 + happiness_a_3)

    optimum_happiness_t = 0
    for day in range(4, days + 1):
        optimum_happiness_t += np.random.normal(10, 5)

    optimum_happiness += optimum_happiness_t

    if happiness_a >= happiness_b and happiness_a >= happiness_c:
        total_happiness += optimum_happiness_t
    elif happiness_b >= happiness_a and happiness_b >= happiness_c:
        for day in range(4, days + 1):
            total_happiness += np.random.normal(8, 4)
    else:
        for day in range(4, days + 1):
            total_happiness += np.random.normal(5, 2.5)

    regret = optimum_happiness - total_happiness

    return optimum_happiness, total_happiness, regret, None


def exploit_one(days, mean, std, mean_max, std_max):
    optimum_happiness = 0
    total_happiness = 0

    if mean == mean_max and std == std_max:
        for _ in range(days):
            happiness = np.random.normal(mean, std)
            total_happiness += happiness
        optimum_happiness = total_happiness

    else:
        for _ in range(days):
            happiness = np.random.normal(mean, std)
            total_happiness += happiness

            happiness_o = np.random.normal(mean_max, std_max)
            optimum_happiness += happiness_o

    regret = optimum_happiness - total_happiness

    return optimum_happiness, total_happiness, regret, None


def e_first(days, epsilon=0.1):

    explore_days = round(days * epsilon)
    optimum_happiness_explore, total_happiness_explore, regret_explore, avg_happiness_arr = explore(explore_days)
    max_index = np.argmax(avg_happiness_arr)
    optimum_happiness_exploit, total_happiness_exploit, regret_exploit, _ = \
        exploit_one(days - explore_days, *parameters[max_index], *parameters[0])

    optimum_happiness = optimum_happiness_explore + optimum_happiness_exploit
    total_happiness = total_happiness_explore + total_happiness_exploit
    regret = optimum_happiness - total_happiness

    return optimum_happiness, total_happiness, regret, None


def e_greedy(days, epsilon=0.1):

    total_happiness = 0
    optimum_happiness = 0

    a = b = c = 0
    total_happiness_a = total_happiness_b = total_happiness_c = 0

    for _ in range(days):
        random_value = np.random.rand()

        happiness_a = np.random.normal(10, 5)
        optimum_happiness += happiness_a

        if random_value <= 0.1:
            # explore
            random_value_1 = np.random.rand()

            if random_value_1 <= 1 / 3:
                total_happiness += happiness_a
                total_happiness_a += happiness_a
                a += 1
            elif random_value <= 2 / 3:
                happiness_b = np.random.normal(8, 4)
                total_happiness += happiness_b
                total_happiness_b += happiness_b
                b += 1
            else:
                happiness_c = np.random.normal(5, 2.5)
                total_happiness += happiness_c
                total_happiness_c += happiness_c
                c += 1
        else:
            # exploit
            a_rate = (total_happiness_a + 10 ** -7) / (a + 10 ** -7)
            b_rate = (total_happiness_b + 10 ** -7) / (b + 10 ** -7)
            c_rate = (total_happiness_c + 10 ** -7) / (c + 10 ** -7)

            if a_rate >= b_rate and a_rate >= c_rate:
                total_happiness += happiness_a
                total_happiness_a += happiness_a
                a += 1
            elif b_rate >= a_rate and b_rate >= c_rate:
                happiness_b = np.random.normal(8, 4)
                total_happiness += happiness_b
                total_happiness_b += happiness_b
                b += 1
            else:
                happiness_c = np.random.normal(5, 2.5)
                total_happiness += happiness_c
                total_happiness_c += happiness_c
                c += 1

    regret = optimum_happiness - total_happiness

    return optimum_happiness, total_happiness, regret, None


def simulate(experiments, func, days):
    optimum_happiness_arr = []
    total_happiness_arr = []
    regret_arr = []

    for _ in range(experiments):
        optimum_happiness, total_happiness, regret, arr = func(days)
        optimum_happiness_arr.append(optimum_happiness)
        total_happiness_arr.append(total_happiness)
        regret_arr.append(regret)

    optimum_happiness_arr = np.array(optimum_happiness_arr)
    total_happiness_arr = np.array(total_happiness_arr)
    regret_arr = np.array(regret_arr)

    return optimum_happiness_arr.mean(), total_happiness_arr.mean(), regret_arr.mean()


def display(policy, optimum_happiness, total_happiness, regret):
    print(policy)
    print("Optimum happiness:", optimum_happiness)
    print("Total happiness:", total_happiness)
    print("Regret:", regret)
    print("\n")


def main():
    num_experiments = 1000

    optimum_happiness, total_happiness, regret = simulate(num_experiments, explore, 300)
    display("Exploration only policy", optimum_happiness, total_happiness, regret)

    optimum_happiness, total_happiness, regret = simulate(num_experiments, exploit, 300)
    display("Exploitation only policy", optimum_happiness, total_happiness, regret)

    optimum_happiness, total_happiness, regret = simulate(num_experiments, e_first, 300)
    display("e_first policy", optimum_happiness, total_happiness, regret)

    optimum_happiness, total_happiness, regret = simulate(num_experiments, e_greedy, 300)
    display("e_greedy policy", optimum_happiness, total_happiness, regret)


if __name__ == "__main__":
    parameters = [(10, 5), (8, 4), (5, 2.5)]
    main()
