# genetic_algorithm.py

import csv
from Player import Player
from blackjack import game
from simplex import Network
import random as rand
import numpy as np
import json
import uuid
import matplotlib.pyplot as plt

y_values = []


class GeneticAlgorithm:
    def __init__(self, population_size: int = 250, win_rate: float = 1.0, mutation_prob: float = 0.1,
                 fitness_rounds: int = 10000, fitnesses: list = []):
        self.id = str(uuid.uuid4())  # So that we can individually identify each genetic algorithm we run
        self.population_size = population_size
        self.mutation_prob = mutation_prob
        self.fitness_rounds = fitness_rounds
        self.population = []
        self.win_rate = win_rate
        self.fitnesses = fitnesses

    def initial_save(self):
        properties = {
            "id": self.id,
            "population_size": self.population_size,
            "fitness_rounds": self.fitness_rounds,
            "win_rate": self.win_rate,
            "actions": self.fitnesses

        }
        return properties


# this method creates a matrix of random values whose shape is a parameter tuple (e.g. (2,4))
def getRandMatrix(shape, limit):
    R = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            R[i][j] = rand.uniform(-limit, limit)
    return R


# this method creates a matrix of random 1's and 0's the same shape as X
# the probability of a one appearing is given by the one_rate parameter
def getRandBinaryMatrix(shape, one_rate):
    B = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            r = rand.random()
            if r < one_rate:
                B[i][j] = 1
            else:
                B[i][j] = 0
    return B


# takes a matrix and changes values to random ones based on the mutation rate parameter
def mutate(X, mutation_rate):
    B = getRandBinaryMatrix(X.shape, mutation_rate)
    R = getRandMatrix(X.shape, 1)
    return X + R * B


# accepts an array of SNNs (and their structure) and uses the cost function to return the best performing network
def getMaxNetwork(network_array):
    max_network = network_array[0]
    max_network_cost = cost_blackjack(max_network)
    for i in range(len(network_array)):
        if cost_blackjack(network_array[i]) > max_network_cost:
            max_network = network_array[i]
            max_network_cost = cost_blackjack(max_network)
    return max_network


# accepts a network and randomly adds values to some weight elements in the weight matrices based on a mutation rate
def mutateNetwork(network, mutation_rate):
    mutant_network = Network(network.layers[0].dim, network.layers[1].dim, network.layers[2].dim)
    mutant_network.layers[1].weight_matrix = mutate(network.layers[1].weight_matrix, mutation_rate)
    mutant_network.layers[2].weight_matrix = mutate(network.layers[2].weight_matrix, mutation_rate)
    return mutant_network


# accepts a network and returns a metric that measures the network's performance in blackjack
def cost_blackjack(network):
    AI = Player('AI', network=network)

    # geneticAlg1 = GeneticAlgorithm(20,0,0.05,10000,[])
    stats = AI.getPlayerPerformanceLearnt(10, False, None)
    # geneticAlg1.fitnesses = stats[3]
    # geneticAlg1.win_rate = stats[0]
    # geneticAlg1.initial_save()
    win_rate = stats[0]
    ave_bank = stats[1]
    ave_reward = stats[2]
    cost = win_rate + ave_bank / 1000.0 + 1.1 * ave_reward
    return cost


# creates a generation of networks
# gen_size is the number of networks in generation, and h_l_s is the hidden layer size (recommended 20)
def createGeneration(gen_size, hidden_layer_size):
    models = []
    for i in range(gen_size):
        models.append(Network(2, hidden_layer_size, 4))
    return models


# accepts a generation of networks and trains them based on a mutation rate (recommended 0.05)
# epoch is the number of training iterations for a single generation (recommeded 200)
# print_info is boolean: should it print data every 10 epochs or not 
def trainGeneration(models, epoch, mutation_rate, print_info, strategy):
    # setting plot variables
    (fig, ax) = plt.subplots(1, 1)
    [train_plot] = ax.plot([], [], color='green', linestyle='-', linewidth=0.7, label='train')
    ax.set_xlim(0, epoch)
    ax.set_xlabel('epoch')

    sizeOfStrategy = 0

    with open('genetic_algorithm.json3', 'a') as file:
        for i in range(len(strategy)):
            for j in range(len(strategy[i])):
                sizeOfStrategy = sizeOfStrategy + 1

        ax.set_ylim(0, sizeOfStrategy)
        ax.set_ylabel('training rate')
        ax.legend()

        file.write('[')

        for i in range(epoch):
            geneticAlg1 = GeneticAlgorithm(20, 0, 0.05, 10000, [])

            writer = csv.writer(file)
            max_network = getMaxNetwork(models)
            AI = Player('AI', network=max_network)
            stats = AI.getPlayerPerformanceLearnt(10, False, strategy)
            with open('evol_neural_net2.csv', 'a') as file:
                file.write(str(i))
            geneticAlg1.fitnesses = stats[3]
            geneticAlg1.win_rate = stats[0]
            properties = geneticAlg1.initial_save()

            with open('genetic_algorithm3.json', 'a') as file:
                file.write(json.dumps(properties))
                file.write('\n')
                file.write(',')
            win_rate = stats[0]
            ave_bank = stats[1]
            if print_info == True and i % 10 == 0: print(
                "Epoch: " + str(i) + " - Win rate: " + str(round(win_rate * 100.0, 1)))
            for i in range(len(models)):
                models[i] = mutateNetwork(max_network, mutation_rate * (0.60 - (win_rate / 10.0)) / 0.60)

            if stats[5]:

                learnt_actions = []

                # print plot
                for x in range(len(stats[4])):
                    for y in range(len(stats[4][x])):
                        if stats[4][x][y] != 'a':
                            learnt_actions.append(stats[4][x][y])
                y_values.append(len(learnt_actions))

                # checking for strategy
                converged = False
                for x in range(len(stats[4])):
                    for y in range(len(stats[4][x])):
                        if stats[4][x][y] == 'a':

                            converged = False
                            break
                        else:
                            converged = True
                    if not converged:
                        break
                with open('EAStrategy5.txt', 'w') as f:

                    for item in stats[4]:
                        f.write("%s\n" % item)
                if converged:
                    break
    plt.plot(y_values)
    plt.savefig('plot3.png')
    plt.show()
    with open('genetic_algorithm.json3', 'a') as file:
        file.write(']')
