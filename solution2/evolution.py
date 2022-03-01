from solution2.mfea import *
from random import sample

def crossover_mutate(parent1: Individual, parent2: Individual, n_relays, pc=0.7, pm=0.2):
    # """
    # Hàm lai ghép và đột biến
    # :param parent1: các thể cha 1
    # :param parent2: cá thể cha 2
    # :param n_relays: Số lượng relays
    # :param pc: Hệ số lai ghép
    # :param pm: Hệ số đột biến
    # :return: Danh sách các cá thể con
    # """
    result = []

    # lai ghép
    rc = np.random.random()
    if (parent1.skill_factor == parent2.skill_factor) or (rc < pc):
        t = sample(range(n_relays + 1, len(parent1.genes)), 2)
        t.sort()
        [t1, t2] = t
        child1 = parent1.genes.copy()
        child2 = parent2.genes.copy()

        child1[t1:t2] = parent2.genes[t1:t2]
        child2[t1:t2] = parent1.genes[t1:t2]

        indiv_child1 = Individual(child1)
        indiv_child2 = Individual(child2)

        # Cập nhật skill fator cho con 1
        select_skill = np.random.random()
        if(select_skill <= 0.5):
            indiv_child1.skill_factor = parent1.skill_factor
        else:
            indiv_child1.skill_factor = parent2.skill_factor

        # Cập nhật skill fator cho con 2
        select_skill = np.random.random()
        if(select_skill <= 0.5):
            indiv_child2.skill_factor = parent1.skill_factor
        else:
            indiv_child2.skill_factor = parent2.skill_factor

        # add
        result.append(indiv_child1)
        result.append(indiv_child2)

    # Đột biến
    rm = np.random.random()
    if (rm < pm):
        child1 = mutate(parent1, n_relays)
        child2 = mutate(parent2, n_relays)
        result.append(child1)
        result.append(child2)
    return result


def mutate(indiv:Individual, n_relays):
    # """
    # :param indiv: Cá thể cha đột biến
    # :param n_relays: Số lượng ralays
    # :return: Cá thể đột biến
    # """
    genes = indiv.genes.copy()
    vitri = np.random.randint(n_relays + 1, len(genes))
    giatri = np.random.randint(1, len(genes))

    genes[vitri] = giatri
    return Individual(genes)

def evolution(pop:Population, n_relays, pc=0.7, pm=0.2, MAX_LEN=100):
    # """
    # Hàm tiến hóa
    # :param pop: Quần thế ban đầu
    # :param n_relays:
    # :param pc:
    # :param pm:
    # :param MAX_LEN:
    # :return:
    # """
    indivs_child = []
    while (len(indivs_child) < MAX_LEN):
        try:
            parent1, parent2 = sample(pop.individuals, 2)
            indivs_child += crossover_mutate(parent1, parent2, n_relays, pc, pm)
        except:
            print("individuals in population < 2")

    pop.add(indivs_child)
    pop.reset_param()
    pop.selection(MAX_LEN)