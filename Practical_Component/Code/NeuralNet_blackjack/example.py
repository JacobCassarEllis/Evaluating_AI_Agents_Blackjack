from genetic_algorithm import createGeneration
from genetic_algorithm import trainGeneration
from genetic_algorithm import getMaxNetwork
from Player import Player
import matplotlib.pyplot as plt
from tree import *
from blackjack import *
import pickle

strategy = [['S', 'S', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['S', 'S', 'S', 'a', 'a', 'a', 'a', 'a', 'H', 'a'],
['S', 'S', 'H', 'S', 'H', 'H', 'H', 'H', 'H', 'H'],
['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
['H', 'H', 'S', 'H', 'S', 'H', 'H', 'H', 'H', 'H'],
['S', 'H', 'S', 'S', 'S', 'H', 'D', 'H', 'H', 'H'],
['S', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
['S', 'S', 'S', 'S', 'D', 'S', 'S', 'D', 'H', 'H'],
['D', 'D', 'S', 'H', 'D', 'S', 'S', 'H', 'H', 'H'],
['D', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'S', 'H'],
['S', 'H', 'S', 'H', 'S', 'S', 'H', 'H', 'H', 'S'],
['H', 'D', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'S'],
['H', 'D', 'H', 'H', 'H', 'D', 'H', 'S', 'H', 'S'],
['H', 'S', 'S', 'H', 'S', 'H', 'H', 'H', 'H', 'S'],
['S', 'D', 'H', 'D', 'H', 'S', 'H', 'H', 'H', 'H'],
['H', 'S', 'S', 'S', 'S', 'S', 'S', 'H', 'S', 'H'],
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'S'],
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'D', 'H'],
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'a'],
['H', 'D', 'D', 'H', 'D', 'H', 'H', 'H', 'H', 'H'],
['H', 'H', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'a'],
['H', 'H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H'],
['H', 'a', 'H', 'H', 'H', 'H', 'H', 'H', 'D', 'H'],
['H', 'D', 'H', 'H', 'H', 'H', 'H', 'a', 'H', 'H'],
['H', 'H', 'H', 'H', 'a', 'H', 'H', 'H', 'H', 'a'],
['H', 'H', 'P', 'H', 'S', 'P', 'P', 'P', 'H', 'P'],
['P', 'H', 'D', 'P', 'P', 'P', 'D', 'P', 'H', 'P'],
['H', 'H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H'],
['H', 'S', 'P', 'H', 'H', 'S', 'H', 'H', 'H', 'H'],
['D', 'H', 'H', 'D', 'H', 'D', 'H', 'H', 'H', 'H'],
['H', 'H', 'D', 'H', 'H', 'H', 'D', 'S', 'H', 'H'],
['H', 'H', 'H', 'S', 'H', 'H', 'H', 'H', 'S', 'H'],
['P', 'H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H'],
['S', 'H', 'S', 'S', 'H', 'H', 'H', 'H', 'H', 'D'],
['H', 'H', 'H', 'S', 'H', 'S', 'H', 'H', 'H', 'H'],
['S', 'H', 'H', 'S', 'S', 'S', 'H', 'S', 'S', 'S']]


strategy2 = [['S', 'a', 'a', 'a', 'a', 'S', 'a', 'S', 'a', 'a'],
['S', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['S', 'S', 'S', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['S', 'H', 'S', 'H', 'H', 'a', 'H', 'H', 'H', 'a'],
['S', 'H', 'S', 'H', 'S', 'H', 'H', 'H', 'S', 'a'],
['S', 'S', 'S', 'H', 'H', 'S', 'H', 'H', 'H', 'H'],
['H', 'S', 'S', 'S', 'D', 'H', 'H', 'H', 'H', 'H'],
['H', 'S', 'H', 'S', 'H', 'S', 'S', 'H', 'H', 'H'],
['S', 'H', 'S', 'D', 'S', 'S', 'H', 'S', 'H', 'H'],
['S', 'S', 'S', 'S', 'H', 'S', 'H', 'H', 'H', 'H'],
['D', 'S', 'D', 'S', 'D', 'S', 'S', 'S', 'H', 'D'],
['S', 'H', 'S', 'S', 'S', 'S', 'H', 'H', 'D', 'S'],
['S', 'S', 'H', 'S', 'S', 'H', 'S', 'S', 'H', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'H', 'S', 'S'],
['S', 'S', 'S', 'S', 'D', 'S', 'S', 'H', 'S', 'H'],
['H', 'S', 'S', 'S', 'H', 'D', 'S', 'S', 'S', 'D'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['H', 'H', 'H', 'H', 'H', 'a', 'H', 'H', 'H', 'a'],
['D', 'D', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'a'],
['H', 'H', 'H', 'H', 'D', 'a', 'a', 'D', 'H', 'a'],
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'a', 'H', 'H'],
['H', 'H', 'H', 'H', 'H', 'a', 'H', 'a', 'H', 'H'],
['H', 'H', 'a', 'H', 'H', 'H', 'H', 'H', 'H', 'a'],
['H', 'D', 'H', 'H', 'a', 'a', 'H', 'H', 'H', 'a'],
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'a'],
['H', 'H', 'H', 'H', 'H', 'a', 'a', 'a', 'D', 'a'],
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'a'],
['P', 'P', 'a', 'P', 'P', 'a', 'P', 'a', 'P', 'P'],
['P', 'a', 'P', 'P', 'P', 'P', 'P', 'a', 'P', 'a'],
['P', 'P', 'P', 'a', 'P', 'P', 'P', 'P', 'P', 'a'],
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'a'],
['P', 'P', 'a', 'a', 'P', 'P', 'a', 'P', 'P', 'a'],
['P', 'P', 'P', 'P', 'P', 'P', 'a', 'a', 'P', 'a'],
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'a']]

strategy3 = [['S', 'a', 'a', 'a', 'a', 'a', 'a', 'a,', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['S', 'S', 'S', 'a', 'a', 'a', 'a', 'S', 'a', 'S'],
['S', 'H', 'H', 'S', 'a', 'a', 'a', 'a', 'H', 'a'],
['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
['S', 'H', 'D', 'D', 'H', 'S', 'a', 'H', 'H', 'H'],
['S', 'H', 'S', 'H', 'S', 'H', 'S', 'H', 'H', 'H'],
['H', 'H', 'H', 'H', 'S', 'H', 'H', 'S', 'H', 'H'],
['S', 'S', 'H', 'S', 'S', 'P', 'P', 'S', 'S', 'H'],
['H', 'H', 'H', 'H', 'H', 'H', 'H', 'S', 'H', 'H'],
['S', 'H', 'D', 'S', 'S', 'H', 'H', 'H', 'S', 'H'],
['H', 'S', 'S', 'H', 'S', 'H', 'H', 'S', 'H', 'H'],
['H', 'S', 'S', 'S', 'S', 'S', 'H', 'S', 'S', 'H'],
['S', 'S', 'S', 'H', 'H', 'H', 'H', 'S', 'S', 'H'],
['H', 'D', 'S', 'S', 'S', 'D', 'S', 'H', 'H', 'D'],
['S', 'S', 'D', 'S', 'S', 'H', 'H', 'H', 'H', 'S'],
['S', 'S', 'H', 'S', 'S', 'D', 'H', 'S', 'S', 'S'],
['S', 'S', 'S', 'H', 'S', 'S', 'S', 'S', 'S', 'S'],
['a', 'a', 'H', 'H', 'H', 'a', 'D', 'H', 'H', 'H'],
['H', 'H', 'H', 'H', 'H', 'a', 'a', 'a', 'H', 'H'],
['H', 'D', 'a', 'a', 'H', 'a', 'H', 'a', 'H', 'a'],
['H', 'a', 'H', 'H', 'a', 'a', 'H', 'a', 'H', 'a'],
['a', 'a', 'H', 'a', 'a', 'H', 'H', 'a', 'H', 'a'],
['a', 'D', 'H', 'a', 'H', 'H', 'a', 'H', 'H', 'a'],
['H', 'a', 'H', 'H', 'a', 'a', 'a', 'a', 'H', 'H'],
['a', 'a', 'H', 'D', 'H', 'a', 'a', 'H', 'H', 'H'],
['a', 'H', 'H', 'a', 'a', 'a', 'a', 'H', 'H', 'a'],
['P', 'P', 'P', 'P', 'P', 'H', 'P', 'P', 'P', 'P'],
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
['P', 'P', 'P', 'a', 'P', 'P', 'P', 'P', 'P', 'a'],
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'a', 'P', 'P'],
['P', 'P', 'P', 'P', 'P', 'a', 'P', 'P', 'P', 'P'],
['P', 'P', 'P', 'P', 'P', 'a', 'P', 'P', 'P', 'P'],
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],

]



# constants
GEN_SIZE =30
HIDDEN_LAYER_SIZE = 100
MUTATION_RATE = 0.5

with open('gamblerAI', 'wb') as f:
    # create and train generation
    models = createGeneration(GEN_SIZE, HIDDEN_LAYER_SIZE)

trainGeneration(models, 30000, MUTATION_RATE, True, strategy3)

pickle.dump(models, f)
# creating user and AI 
gambling_addict = Player('AI', network=getMaxNetwork(models))
# kayli = Player('Kayli')

# AI plays 10 games
# for i in range(10):
# 	gameLearnt(gambling_addict, 4, True)
# print(1.0 * gambling_addict.wins / gambling_addict.games, gambling_addict.bank)

# # user plays 10 games
# for i in range(10):
# 	game(kayli, 4, True)
# print(1.0 * kayli.wins / kayli.games, kayli.bank)
