import progressbar
import pandas as pd
import matplotlib.pyplot as plt
from blackjack import Blackjack
from player import LoadedPlayer
from q_learning import QLearningBlackjackPolicy

'''
for i in range(100):
	player = LoadedPlayer('basicstrategy.csv', 0)

	blackjack_game = Blackjack([player], 1, 1, 8, 50)
	blackjack_game.play(50000)

	print("Num Wins: " + str(player.num_matches_won))
	print("Num Losses: " + str(player.num_matches_lost))
	print("Num Draws: " + str(player.num_matches_drawn))
	print("Amount Chips: " + str(player.chips))
	print(" ")
'''

num_testing_games = 100000

subfolder = '33c41535-5bf8-42c4-a6e6-688430388343'

file_1 = '782c6c21-735f-434a-8066-c4c2e5a450d3' # Least Losses
file_2 = '5ceb1f48-dc6a-417f-8870-c982a42c7aba' # Most Wins
file_3 = '2a870eb4-bf9b-4666-a8a8-3b55db56a8ed' # Best Net Chips

best_l = QLearningBlackjackPolicy.load_iterations_as_static_players(file_1, subfolder, True)
best_w = QLearningBlackjackPolicy.load_iterations_as_static_players(file_2, subfolder, True)
best_c = QLearningBlackjackPolicy.load_iterations_as_static_players(file_3, subfolder, True)

players = [ player for (variation, _, _, _) in [best_l, best_w, best_c] for player in variation ]

blackjack_testing = Blackjack(players, 1, file_1, 8, 50)
for i in progressbar.progressbar(range(1, num_testing_games + 1)): 
	blackjack_testing.play_same_conditions(1)

# To output the results as a csv and a prettytable
output_table = {
	'learning_rate': list(),
	'discount_factor': list(),
	'exploration_rate': list(),
	'wins': list(),
	'losses': list(),
	'net_chips': list()
}

loaded_players = [ best_l, best_w, best_c ]

wins, losses, net_chips = list(), list(), list()
for player in loaded_players:
	current_wins, current_losses, current_chips = list(), list(), list()
	for progression in player[0]:
		current_wins.append(progression.num_matches_won)
		current_losses.append(progression.num_matches_lost)
		current_chips.append(progression.chips)
	wins.append(current_wins)
	losses.append(current_losses)
	net_chips.append(current_chips)
	output_table['learning_rate'].append(player[1])
	output_table['discount_factor'].append(player[2])
	output_table['exploration_rate'].append(player[3])
	output_table['wins'].append(current_wins[-1])
	output_table['losses'].append(current_losses[-1])
	output_table['net_chips'].append(current_chips[-1])

output_dataframe = pd.DataFrame(output_table)
output_dataframe.sort_values(['losses', 'wins', 'net_chips'], ascending=[True, False, False], inplace=True)
output_dataframe.to_csv('q_top-performing-params.csv')
print(output_dataframe)

save_iteration_index = [0]
for i in range(1, 1000000 + 1):
	if (i <= 10000 and i % 1000 == 0):
		save_iteration_index.append(i)
	elif (i <= 100000 and i % 10000 == 0):
		save_iteration_index.append(i)
	elif (i % 100000 == 0):
		save_iteration_index.append(i)

# Constructing the graphs to be outputted
(fig, axs) = plt.subplots(1, 3)
fig.set_size_inches(15, 4.8)

# Labels
labels = [ 'Least Losses', 'Most Wins', 'Best Net Chips' ]

for i in range(len(loaded_players)):
	curr_w, curr_l, curr_c = wins[i], losses[i], net_chips[i]
	curr_lr, curr_df, curr_er = loaded_players[i][1], loaded_players[i][2], loaded_players[i][3]

	curr_label = labels[i] + ' (' + str(curr_lr) + ', ' + str(curr_df) + ', ' + str(curr_er) + ')'
	#color = ('#' + str(hex(random.randint(0, 255))).split('x')[-1] 
	#             + str(hex(random.randint(0, 255))).split('x')[-1]  
	#			 + str(hex(random.randint(0, 255))).split('x')[-1])
	[ _wins ] = axs[0].plot(
		save_iteration_index,
		curr_w,
		#color=color,
		linestyle='-',
		linewidth=1,
		label=curr_label)
	[ _losses ] = axs[1].plot(
		save_iteration_index,
		curr_l,
		#color=color,
		linestyle='-',
		linewidth=1,
		label=curr_label)
	[ _net_money ] = axs[2].plot(
		save_iteration_index,
		curr_c,
		#color=color,
		linestyle='-',
		linewidth=1,
		label=curr_label)

# Wins
#axs[0].set_xlim(0, max(save_iteration_index))
#axs[0].set_ylim(0, num_testing_games)
axs[0].set_xlabel('Training games played')
axs[0].set_ylabel('Wins')
axs[0].grid(True)
axs[0].set_title('Training Win Progression')
axs[0].legend()

# Losses
#axs[1].set_xlim(0, max(save_iteration_index))
#axs[1].set_ylim(0, num_testing_games)
axs[1].set_xlabel('Training games played')
axs[1].set_ylabel('Losses')
axs[1].grid(True)
axs[1].set_title('Training Loss Progression')
axs[1].legend()

# Losses
axs[2].set_xlabel('Training games played')
axs[2].set_ylabel('Net Chips')
axs[2].grid(True)
axs[2].set_title('Training Chips Progression')
axs[2].legend()

fig.canvas.set_window_title('Training Progress')
fig.tight_layout()
fig.show()
fig.savefig('training-progress-qlearning_best')

pass