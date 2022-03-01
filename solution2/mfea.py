import numpy as np

from solution2.func import *

class Individual:
    def __init__(self, genes, skill_factor=-1):
        # """
        # :param genes: Danh sách các node cha
        # :param skill_factor: Cá thể thuộc bài toán 0, 1,.. nếu là -1 chưa chọn
        # """
        self.genes = np.array(genes)

        self.skill_factor = skill_factor
        self.list_cost = []
        self.list_rank = []

    def set_cost(self, pop_configs):
        # """
        # :param pop_configs: Config cua cac bai toan
        # :return: list cost cua tung bai toan
        # """
        if (len(self.list_cost) == 0):
            list_cost = []
            for problem in range(len(pop_configs)):
                genes_encode = encode(self.genes, pop_configs[problem])
                list_cost.append(Energy_consumption_sensor(genes_encode, pop_configs[problem]))
            self.list_cost = list_cost
        return self.list_cost

    def get_cost(self, problem=-1):
        if(problem == -1):
            return self.list_cost[self.skill_factor]
        if (len(self.list_cost) == 0):
            return MAX_ENERRY
        return self.list_cost[problem]

    def set_rank(self, rank=[]):
        if(len(rank) == 0):
            return self.list_rank
        else:
            self.list_rank = rank
        # self.skill_factor = self.list_rank.index(self.list_rank.min())

    def get_rank(self, problem):
        return self.list_rank[problem]

    def get_scalar_fitness(self):
        return 1/self.list_rank[self.skill_factor]

    def get_individual(self):
        return self.genes

    def copy(self):
        temp_indiv = Individual(self.genes.copy())
        temp_indiv.skill_factor = self.skill_factor
        temp_indiv.list_cost = self.list_cost
        temp_indiv.list_rank = self.list_rank
        return temp_indiv

class Population:
    def __init__(self, n_sensor, n_relay, individuals, pop_configs):
        self.individuals = individuals
        self.__length = len(individuals)
        self.n_sensor = n_sensor
        self.n_relay = n_relay
        self.pop_configs = pop_configs

        self.__get_fittest = []

    @property
    def length(self):
        self.__length = len(self.individuals)
        return self.__length

    def add(self, indivs):
        if(len(indivs) > 0):
            self.__get_fittest = []
            for indiv in indivs:
                self.individuals.append(indiv)
        return self.individuals

    def random_indivs(self, nums):
        self.__get_fittest = []
        arrs = np.random.randint(1, self.n_relay + self.n_sensor + 1, (nums, self.n_sensor))
        indivs = []
        for x in arrs:
            # 0 | 0 0 0.. | ****
            indiv = np.concatenate((np.zeros(self.n_relay + 1), x))
            indivs.append(Individual(indiv))
        self.add(indivs)

    def remove(self, indivs):
        if len(indivs) > 0:
            self.__get_fittest = []
            for indiv in indivs:
                self.individuals.remove(indiv)

    def get_fittest(self):
        if (len(self.__get_fittest) == 0):
            best_indivs = [self.individuals[0].copy() for _ in range(len(self.pop_configs))]
            individuals = self.individuals

            for problem in range(len(self.pop_configs)):
                # gia tri dau
                for indiv in individuals:
                    if (indiv.skill_factor == problem):
                        best_indivs[problem] = indiv.copy()
                        break

                for indiv in individuals:
                    if (indiv.skill_factor == problem) or (indiv.skill_factor == -1):
                        a = indiv.get_cost(problem)
                        b = best_indivs[problem].get_cost(problem)
                        if (b >= a):
                            best_indivs[problem] = indiv.copy()
            self.__get_fittest = best_indivs
        return self.__get_fittest

    # Chọn lọc các thể
    def selection(self, max_len_indiv):
        new_indivs = []
        best_indivs = []
        for problem in range(len(self.pop_configs)):
            local_indivs = [indiv.copy() for indiv in self.individuals if indiv.skill_factor == problem]
            if (len(local_indivs) <= max_len_indiv):
                new_indivs += local_indivs
            else:
                arr_cost = [(i, local_indivs[i].get_scalar_fitness()) for i in range(len(local_indivs))]
                arr_cost.sort(key=lambda x: x[1], reverse=True)
                index_cost = [i[0] for i in arr_cost[:max_len_indiv]]
                new_indivs += [local_indivs[i] for i in index_cost]
                best_indivs.append(local_indivs[index_cost[0]])
        self.individuals = new_indivs

    def reset_param(self):
        # cost
        for indiv in self.individuals:
            indiv.set_cost(self.pop_configs)

        # rank
        matrix_rank = []
        for i in range(len(self.pop_configs)):
            list_cost_local = [x.get_cost(i) for x in self.individuals]
            matrix_rank.append(reset_rank(list_cost_local))

        matrix_rank = np.array(matrix_rank)
        for i in range(self.length):
            self.individuals[i].set_rank(list(matrix_rank[:, i]))

        # skill factor
        for indiv in self.individuals:
            if(indiv.skill_factor == -1):
                indiv.skill_factor = indiv.list_rank.index(min(indiv.list_rank))