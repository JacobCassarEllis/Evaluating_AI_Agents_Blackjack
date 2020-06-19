import sys, os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import progressbar
import math
from genetic_algorithms import *
from blackjack import *
from player import *
from q_learning import *

def calculate_std(values):
	pop_size = len(values)
	pop_mean = sum(values) / pop_size

	summation = 0
	for value in values:
		summation += (value - pop_mean) ** 2

	variance = summation / pop_size

	return math.sqrt(variance)

testing_rounds = 100000

q_learning_folder = '33c41535-5bf8-42c4-a6e6-688430388343'
evolutionary_nn_folder = os.path.join(os.getcwd(), 'evolutionary_neural_network')

q_learning_id = '2a870eb4-bf9b-4666-a8a8-3b55db56a8ed'
ga_id = 'cea6fbd0-53d4-4f83-859b-0ead49fc52a1'

ql = QLearningBlackjackPolicy.load_iterations_as_static_players(q_learning_id, q_learning_folder)[-1]
ga = GeneticAlgorithm.load_best_chromosome_of_each_generation(ga_id)[0][-1][0]
en = LoadedPlayer(evolutionary_nn_folder + '/EAStrategy5Final.csv', 0)

mimic = MimickTheDealerPlayer(0)
nev_b = NeverBustPlayer(0)
rando = RandomPlayer(0)

basic = LoadedPlayer(os.getcwd() + '/basicstrategy.csv', 0)

players = [ ql, ga, en, mimic, nev_b, rando, basic ]
player_names = [ 'Q-L', 'G.A.', 'Ev. NN.', 'Mimic', 'Never B.', 'Random', 'Basic S.' ]
#players = [ ql, ga, mimic, nev_b, rando, basic ]
#player_names = [ 'Q-L', 'G.A.', 'Mimic', 'Never B.', 'Random', 'Basic S.' ]
players_w = [ [] for player in players ]
players_l = [ [] for player in players ]
players_c = [ [] for player in players ]
for i in range(10):
	for j in progressbar.progressbar(range(1, testing_rounds + 1)):
		blackjack_testing = Blackjack(players, 1, 1, 8, 50)
		blackjack_testing.play_same_conditions(1)
	for k in range(len(players)):
		players_w[k].append(players[k].num_matches_won)
		players_l[k].append(players[k].num_matches_lost)
		players_c[k].append(players[k].chips)
		players[k].num_matches_won = 0
		players[k].num_matches_lost = 0
		players[k].chips = 0

output_table = {
	'algorithm_name': list(),
	'mean_wins': list(),
	'std_wins': list(),
	'mean_losses': list(),
	'std_losses': list(),
	'mean_net_chips': list(),
	'std_net_chips': list()
}

for i in range(len(players)):
	curr_w = players_w[i]
	curr_l = players_l[i]
	curr_c = players_c[i]
	output_table['algorithm_name'].append(players[i])
	output_table['mean_wins'].append(sum(curr_w) / len(curr_w))
	output_table['std_wins'].append(calculate_std(curr_w))
	output_table['mean_losses'].append(sum(curr_l) / len(curr_l))
	output_table['std_losses'].append(calculate_std(curr_l))
	output_table['mean_net_chips'].append(sum(curr_c) / len(curr_c))
	output_table['std_net_chips'].append(calculate_std(curr_c))

output_dataframe = pd.DataFrame(output_table)
output_dataframe.to_csv('final-statistics.csv')
print(output_dataframe)

(fig, axs) = plt.subplots(1, 3)
fig.set_size_inches(15, 4.8)

for i in range(len(players)):
	curr_w = players_w[i]
	curr_l = players_l[i]
	curr_c = players_c[i]

	[ wins ] = axs[0].plot(
		[i for i in range(1, 10 + 1)],
		curr_w,
		linestyle='-',
		linewidth=1,
		label=player_names[i])
	[ losses ] = axs[1].plot(
		[i for i in range(1, 10 + 1)],
		curr_l,
		linestyle='-',
		linewidth=1,
		label=player_names[i])
	[ chips ] = axs[2].plot(
		[i for i in range(1, 10 + 1)],
		curr_c,
		linestyle='-',
		linewidth=1,
		label=player_names[i])

axs[0].set_xlabel('Test Index')
axs[0].set_ylabel('Wins')
axs[0].grid(True)
axs[0].set_title('Test Wins')
axs[0].legend(fontsize='small')

axs[1].set_xlabel('Test Index')
axs[1].set_ylabel('Losses')
axs[1].grid(True)
axs[1].set_title('Test Losses')
axs[1].legend(fontsize='small')

axs[2].set_xlabel('Test Index')
axs[2].set_ylabel('Net Chips')
axs[2].grid(True)
axs[2].set_title('Test Net Chips')
axs[2].legend(fontsize='small')

fig.canvas.set_window_title('Algorithm Comparisons')
fig.tight_layout()
fig.show()
fig.savefig('algorithm-comparisons')