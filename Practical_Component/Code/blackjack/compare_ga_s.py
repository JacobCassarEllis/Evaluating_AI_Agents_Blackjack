import sys, os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import progressbar
import math
from genetic_algorithms import *
from blackjack import *
from player import *

def calculate_std(values):
	pop_size = len(values)
	pop_mean = sum(values) / pop_size

	summation = 0
	for value in values:
		summation += (value - pop_mean) ** 2

	variance = summation / pop_size

	return math.sqrt(variance)

folder = os.path.join(os.getcwd(), 'genetic_algorithm')

testing_rounds = 100000

ga_details = list()
loaded_players = list()
actual_players = list()
for path in glob.glob(folder + '\\*.json'):
	id = path.split('\\')[-1].split('.')[0].split('_')[-1]
	ga = GeneticAlgorithm.load_best_chromosome_of_each_generation(id)
	loaded = ga[0][-1]
	player = loaded[0]
	ga_details.append(ga)
	loaded_players.append(loaded)
	actual_players.append(player)

# Setting the data to draw the fitness related stuff for all genetic algorithms

best_fitnesses = list()
avrg_fitnesses = list()
for ga in ga_details:
	current_best_fitnesses = list()
	current_avrg_fitnesses = list()
	for (_, best_f, avrg_f, _) in ga[0]:
		current_best_fitnesses.append(best_f)
		current_avrg_fitnesses.append(avrg_f)
	best_fitnesses.append(current_best_fitnesses)
	avrg_fitnesses.append(current_avrg_fitnesses)

(fig1, axs1) = plt.subplots(1, 2)
fig1.set_size_inches(15, 4.8)

for i in range(len(ga_details)):
	current_best_fs = best_fitnesses[i]
	current_avrg_fs = avrg_fitnesses[i]

	[ bests ] = axs1[0].plot(
		[ i for i in range(len(current_best_fs)) ],
		current_best_fs,
		linestyle='-',
		linewidth=1)
	[ avrgs ] = axs1[1].plot(
		[ i for i in range(len(current_avrg_fs)) ],
		current_avrg_fs,
		linestyle='-',
		linewidth=1)

axs1[0].set_xlabel('Generation index')
axs1[0].set_ylabel('Fitness')
axs1[0].grid(True)
axs1[0].set_title('Best Chromosome Fitness per Generation')

axs1[1].set_xlabel('Generation index')
axs1[1].set_ylabel('Fitness')
axs1[1].grid(True)
axs1[1].set_title('Average Chromosome Fitness per Generation')

fig1.canvas.set_window_title('Fitness Improvement Over Generations')
fig1.tight_layout()
fig1.show()
fig1.savefig('generation-fitness-improvement-all')

# Creating the test to deduce the best performing genetic algorithm and storing data about the test

players_w = [ [] for player in actual_players ]
players_l = [ [] for player in actual_players ]
players_c = [ [] for player in actual_players ]

for i in range(5):
	for j in progressbar.progressbar(range(1, testing_rounds + 1)):
		blackjack_testing = Blackjack(actual_players, 1, 1, 8, 50)
		blackjack_testing.play_same_conditions(1)
	for k in range(len(actual_players)):
		players_w[k].append(actual_players[k].num_matches_won)
		players_l[k].append(actual_players[k].num_matches_lost)
		players_c[k].append(actual_players[k].chips)
		actual_players[k].num_matches_won = 0
		actual_players[k].num_matches_lost = 0
		actual_players[k].chips = 0

output_table = {
	'population_size': list(),
	'crossover_prob': list(),
	'mutation_prob': list(),
	'fitness_rounds': list(),
	'crossover_method': list(),
	'tournament_size': list(),
	'mean_wins': list(),
	'std_wins': list(),
	'mean_losses': list(),
	'std_losses': list(),
	'mean_net_chips': list(),
	'std_net_chips': list()
}

for i in range(len(ga_details)):
	ga = ga_details[i]
	curr_w = players_w[i]
	curr_l = players_l[i]
	curr_c = players_c[i]
	output_table['population_size'].append(ga[1])
	output_table['crossover_prob'].append(ga[2])
	output_table['mutation_prob'].append(ga[3])
	output_table['fitness_rounds'].append(ga[4])
	output_table['crossover_method'].append(ga[5])
	output_table['tournament_size'].append(ga[6])
	output_table['mean_wins'].append(sum(curr_w) / len(curr_w))
	output_table['std_wins'].append(calculate_std(curr_w))
	output_table['mean_losses'].append(sum(curr_l) / len(curr_l))
	output_table['std_losses'].append(calculate_std(curr_l))
	output_table['mean_net_chips'].append(sum(curr_c) / len(curr_c))
	output_table['std_net_chips'].append(calculate_std(curr_c))

output_dataframe = pd.DataFrame(output_table)
#output_dataframe.sort_values(['mean_net_chips', 'std_net_chips', 'mean_losses', 'std_losses', 'mean_wins', 'std_wins'], ascending=[False, True, True, True, False, True], inplace=True)
output_dataframe.to_csv('ga-multiple_params.csv')
print(output_dataframe)

id_best_w = output_dataframe['mean_wins'].idxmax()
id_best_l = output_dataframe['mean_losses'].idxmin()
id_best_c = output_dataframe['mean_net_chips'].idxmax()

best_w = output_dataframe.loc[id_best_w]
best_l = output_dataframe.loc[id_best_l]
best_c = output_dataframe.loc[id_best_c]
bests = [ best_w, best_l, best_c ]

labels = [ 'Most Wins', 'Least Losses', 'Best Net Chips' ]

for i in range(len(bests)):
	print(labels[i])
	print(bests[i])
	print(' ')

reduced_best_fitnesses = list()
reduced_avrg_fitnesses = list()
reduced_chips = list()
best_players = list()
for j in range(len(bests)):
	target_pop_size = bests[j]['population_size']
	target_mut_prob = bests[j]['mutation_prob']
	target_cro_meth = bests[j]['crossover_method']
	target_tou_size = bests[j]['tournament_size']
	labels[j] += (' - ' + str(target_pop_size) + ', ' 
						+ str(target_mut_prob) + ', ' 
						+ str(target_cro_meth) 
						+ ((', ' + str(target_tou_size) if target_tou_size != None else '')))
	for i in range(len(ga_details)):
		current_pop_size = ga_details[i][1]
		current_mut_prob = ga_details[i][3]
		current_cro_meth = ga_details[i][5]
		current_tou_size = ga_details[i][6]
		if (target_pop_size == current_pop_size and
			target_mut_prob == current_mut_prob and
			target_cro_meth == current_cro_meth and
			target_tou_size == current_tou_size):
			reduced_best_fitnesses.append(best_fitnesses[i])
			reduced_avrg_fitnesses.append(avrg_fitnesses[i])
			reduced_chips.append(players_c[i])
			best_players.append(actual_players[i])
			break

(fig2, axs2) = plt.subplots(1, 3)
fig2.set_size_inches(15, 4.8)

for i in range(len(best_players)):
	current_best_fs = reduced_best_fitnesses[i]
	current_avrg_fs = reduced_avrg_fitnesses[i]
	current_chips = reduced_chips[i]

	[ bests ] = axs2[0].plot(
		[ i for i in range(len(current_best_fs)) ],
		current_best_fs,
		linestyle='-',
		linewidth=1,
		label=labels[i])
	[ avrgs ] = axs2[1].plot(
		[ i for i in range(len(current_avrg_fs)) ],
		current_avrg_fs,
		linestyle='-',
		linewidth=1,
		label=labels[i])
	[ chips ] = axs2[2].plot(
		[ i for i in range(1, len(current_chips) + 1) ],
		current_chips,
		linestyle='-',
		linewidth=1,
		label=labels[i])

axs2[0].set_xlabel('Generation index')
axs2[0].set_ylabel('Fitness')
axs2[0].grid(True)
axs2[0].set_title('Best Chromosome Fitness per Generation')
axs2[0].legend(fontsize='small')

axs2[1].set_xlabel('Generation index')
axs2[1].set_ylabel('Fitness')
axs2[1].grid(True)
axs2[1].set_title('Average Chromosome Fitness per Generation')
axs2[1].legend(fontsize='small')

axs2[2].set_xlabel('Test Index')
axs2[2].set_ylabel('Num Chips')
axs2[2].grid(True)
axs2[2].set_title('Num. Chips After Each Test')
axs2[2].legend(fontsize='small')

fig2.canvas.set_window_title('Generation Fitness and Performance')
fig2.tight_layout()
fig2.show()
fig2.savefig('generation-fitness-improvement-top_3')