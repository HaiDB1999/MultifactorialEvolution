from solution2.func import *
from solution2.mfea import *
from solution2.evolution import *
import json

"data/ga-dem10_r25_1_40.json"
paths = ["data/ga-dem10_r25_1_0.json"]

pop_configs = []
for path in paths:
    config = {}
    f = open(path)
    data = json.load(f)
    f.close()

    config['n_relay'] = data['num_of_relays']
    config['n_sensor'] = data['num_of_sensors']
    config['radius'] = data['radius']

    relays = data['relays']
    sensors = data['sensors']
    center = data['center']
    radius = data['radius']

    list_node = [center] + relays + sensors
    list_coordinates = []
    for node in list_node:
        list_coordinates.append([node['x'], node['y'], node['z']])
    list_coordinates = np.array(list_coordinates)
    config['list_coordinates'] = list_coordinates
    pop_configs.append(config)

# khoi tao population
max_n_relays = max(config['n_relay'] for config in pop_configs)
max_n_sensors = max(config['n_sensor'] for config in pop_configs)

# khoi tao gene dau tien
genes_init = np.concatenate([np.zeros(max_n_relays+1), np.random.randint(1, len(list_coordinates), max_n_sensors)])
pop = Population(max_n_sensors, max_n_relays, [Individual(genes_init)], pop_configs)
pop.random_indivs(10)
pop.reset_param()

# arr = []
# for i in range(10):
#   evolution(pop, max_n_relays, 0.3, 1, 100)
#   arr.append([x.get_cost() for x in pop.get_fittest()])
#   print("Lan thu {0}: {1}".format(i, arr[-1]))

print([(indiv.get_cost(0)) for indiv in pop.individuals])

indiv_test = pop.individuals[0]
print(indiv_test.genes)

