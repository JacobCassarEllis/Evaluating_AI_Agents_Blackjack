import sys, os
import random
import matplotlib.pyplot as plt
import uuid
import progressbar
import timeit
import glob
import pandas as pd
from tree import *
from player import *
from q_learning import *

suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
cards = {
	'A': 11,
	'2': 2,
	'3': 3,
	'4': 4,
	'5': 5,
	'6': 6,
	'7': 7,
	'8': 8,
	'9': 9,
	'10': 10,
	'J': 10,
	'Q': 10,
	'K': 10
}

class Card:
	def __init__(self, suit, face, value):
		self.suit = suit
		self.face = face
		self.value = value

	def to_string(self):
		return '{ "suit": "' + str(self.suit) + '", "face": "' + str(self.face) + '", "value": "' + str(self.value) + '" }'

	def __str__(self):
		return self.to_string()

	def __repr__(self):
		return self.to_string()

symbol_to_move_name = {
	'H': 'Hit',
	'S': 'Stand',
	'D': 'Double-down',
	'P': 'Split'
}

class Hand:
	def __init__(self, card_1, card_2, amount_betted):
		self.cards = [card_1, card_2]
		self.has_doubled_down = False
		self.can_split = card_1.face == card_2.face
		self.soft_cards_available = 0
		if card_1.face == 'A' and card_2.face == 'A':
			self.soft_cards_available += 2
		elif (card_1.face == 'A' and card_2.face != 'A') or (card_1.face != 'A' and card_2.face == 'A'):
			self.soft_cards_available += 1
		self.soft_cards_used = 0
		self.amount_betted_on_hand = amount_betted
		self.hand_strength = card_1.value + card_2.value
		if self.hand_strength > 21 and self.has_soft_card_available():
			self.hand_strength -= 10
			self.soft_cards_used += 1

	def has_soft_card_available(self):
		return self.soft_cards_available > self.soft_cards_used

	def add_card(self, card):
		self.cards.append(card)
		self.can_split = False
		self.hand_strength += card.value
		if card.face == 'A':
			self.soft_cards_available += 1
		if self.hand_strength > 21 and self.has_soft_card_available():
			self.hand_strength -= 10
			self.soft_cards_used += 1

	def add_amount_to_bet(self, amount):
		self.amount_betted_on_hand += amount # In case we have a double down

	def get_possible_moves(self):
		if (self.hand_strength > 21 and not self.has_soft_card_available()) or self.hand_strength == 21 or self.has_doubled_down:
			return ['S']
		possible_moves = ['H', 'S']
		if self.can_split:
			possible_moves.append('P')
		if len(self.cards) == 2:
			possible_moves.append('D') # Double down only allowed when player has 2 cards in the hand
		return possible_moves

	def to_string(self):
		lines = ["hand: {"]
		for i in range(len(self.cards)):
			lines.append("card_" + str(i) + ": " + str(self.cards[i]))
		lines.append("}")
		return '\n'.join(lines)

	def __repr__(self):
		return self.to_string()

	def __str__(self):
		return self.to_string()

class Deck:
	def __init__(self, num_packs: int = 1):
		self.cards = []
		for i in range(num_packs):
			for suit in suits:
				for face, value in cards.items():
					self.cards.append(Card(suit, face, value))
		self.drawn_cards = []
		self.num_packs = num_packs
		self.cards_drawn_since_last_shuffle = 0

	def draw_card(self):
		drawn = self.cards.pop(0)
		self.drawn_cards.append(drawn)
		self.cards_drawn_since_last_shuffle += 1
		return drawn

	def add_drawn_cards_back(self):
		self.cards.extend(self.drawn_cards)
		self.drawn_cards = []

	def shuffle_cards(self):
		# From https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/
		# Start from the last element and swap one by one. We don't 
		# need to run for the first element that's why i > 0 
		for i in range(len(self.cards) - 2, 0, -1):
			# Pick a random index from 0 to i 
			j = random.randint(0, i+1)
			# Swap arr[i] with the element at random index 
			self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
		self.cards_drawn_since_last_shuffle = 0

	def to_string(self):
		string_lines = []
		string_lines.append('{')
		string_lines.append('\t"cards": [')
		for card in self.cards:
			if card != self.cards[-1]:
				string_lines.append('\t\t' + card.to_string() + ',')
			else:
				string_lines.append('\t\t' + card.to_string())
		string_lines.append('\t],')
		string_lines.append('\t"drawn_cards": [')
		for card in self.drawn_cards:
			if card != self.drawn_cards[-1]:
				string_lines.append('\t\t' + card.to_string() + ',')
			else:
				string_lines.append('\t\t' + card.to_string())
		string_lines.append('\t],')
		string_lines.append('\t"num_packs": ' + str(self.num_packs))
		string_lines.append('}')
		return '\n'.join(string_lines)

	def __str__(self):
		return self.to_string()

	def __repr__(self):
		return self.to_string()

class Dealer:
	def __init__(self):
		self.up_card = None
		self.down_card = None
		self.soft_cards_available = 0
		self.soft_cards_used = 0
		self.hit_cards = []
		self.hand_strength = 0

	def has_soft_card_available(self):
		return self.soft_cards_available > self.soft_cards_used

	def start_new_turn(self, up_card, down_card):
		self.up_card = up_card
		self.down_card = down_card
		self.hit_cards = []
		self.hand_strength = up_card.value + down_card.value
		self.soft_cards_available = 0
		if up_card.face == 'A' and down_card.face == 'A':
			self.soft_cards_available += 2
		elif (up_card.face == 'A' and down_card.face != 'A') or (up_card.face != 'A' and down_card.face == 'A'):
			self.soft_cards_available += 1
		self.soft_cards_used = 0
		if self.hand_strength > 21 and self.has_soft_card_available():
			self.hand_strength -= 10
			self.soft_cards_used += 1

	def play_turn(self):
		# Dealer strategy used = Hit on soft 17
		if self.hand_strength < 17 or (self.hand_strength == 17 and self.has_soft_card_available()):
			return 'H'
		else:
			return 'S'

	def add_new_card(self, card):
		self.hit_cards.append(card)
		self.hand_strength += card.value
		if card.face == 'A':
			self.soft_cards_available += 1
		if self.hand_strength > 21 and self.has_soft_card_available():
			self.hand_strength -= 10
			self.soft_cards_used += 1

class Blackjack:
	def __init__(self, players: list, minimum_bet: int = 1, maximum_bet: int = 1000, number_of_decks: int = 8, shuffle_every: int = 40):
		self.dealer = Dealer()
		self.players = players
		self.minimum_bet = minimum_bet
		self.maximum_bet = maximum_bet
		self.deck = Deck(number_of_decks)
		self.deck.shuffle_cards()
		self.deck.shuffle_cards()
		self.player_hands = {}
		for player in self.players:
			self.player_hands[player] = ReplacementBinaryTree()
		self.card_count = 0
		self.total_rounds_played = 0
		self.shuffle_every = shuffle_every

	def request_initial_bet_from_players(self):
		initial_bets = {}
		for player in self.players:
			initial_bets[player] = player.place_initial_bet(self.minimum_bet, self.maximum_bet, self.card_count)
		return initial_bets

	def draw_single_card(self):
		card = self.deck.draw_card()
		true_count_denominator = ((self.deck.num_packs * 52) - self.deck.cards_drawn_since_last_shuffle) / 52
		if card.face in ['2', '3', '4', '5', '6']:
			self.card_count += 1 / true_count_denominator
		elif card.face in ['10', 'J', 'Q', 'K', 'A']:
			self.card_count -= 1 / true_count_denominator
		return card

	def draw_round_cards(self, initial_bets: dict):
		for player in self.players:
			card_1 = self.draw_single_card()
			card_2 = self.draw_single_card()
			player_hand = Hand(card_1, card_2, initial_bets[player])
			self.player_hands[player].overwrite_root(player_hand)
		self.dealer.start_new_turn(self.draw_single_card(), self.draw_single_card())

	def request_actions_from_players(self):
		for player in self.players:
			next_hands = self.player_hands[player].get_tree_as_list()
			last_completed_hand = None
			# Keep on requesting the actions from the player for the given hand
			while len(next_hands) != 0:
				target_hand = next_hands[0]
				action = player.play_move(target_hand, self.dealer.up_card)
				# If the player decides to stand
				if action == 'S':
					# Let the current hand be completed and get all of the remaining hands after this hand
					last_completed_hand = target_hand
					next_hands = self.player_hands[player].get_all_hands_after_hand(target_hand)
				# If the player decides to split
				elif action == 'P':
					# Request the money to split from the player
					amount = player.force_amount_to_be_betted(target_hand.amount_betted_on_hand)
					# Build up the two hands which will replace the hand being splitted
					target_hand_card_1 = target_hand.cards[0]
					target_hand_card_2 = target_hand.cards[1]
					new_card_1 = self.draw_single_card()
					new_card_2 = self.draw_single_card()
					output_hand1 = Hand(target_hand_card_1, new_card_1, amount)
					output_hand2 = Hand(target_hand_card_2, new_card_2, amount)
					# Actually perform the replacement
					self.player_hands[player].replace(target_hand, output_hand1, output_hand2)
					# Always keep hands which are not yet completed in the list of hands that need to be evaluated
					if last_completed_hand != None:
						next_hands = self.player_hands[player].get_all_hands_after_hand(last_completed_hand)
					else:
						next_hands = self.player_hands[player].get_tree_as_list()
				# If the player decides to double down
				elif action == 'D':
					amount = player.force_amount_to_be_betted(target_hand.amount_betted_on_hand)
					target_hand.add_amount_to_bet(amount)
					target_hand.add_card(self.draw_single_card())
					target_hand.has_doubled_down = True
				else:
					target_hand.add_card(self.draw_single_card())

	def request_actions_from_dealer(self):
		while self.dealer.play_turn() != 'S':
			self.dealer.add_new_card(self.draw_single_card())

	def give_rewards(self):
		dealer_cards = [self.dealer.up_card, self.dealer.down_card]
		for card in self.dealer.hit_cards:
			dealer_cards.append(card)
		for player in self.players:
			player_hands = self.player_hands[player].get_tree_as_list()
			player_rewards = []
			for hand in player_hands:
				if hand.hand_strength > 21:
					player_rewards.append(0)
				elif hand.hand_strength < self.dealer.hand_strength and self.dealer.hand_strength <= 21:
					player_rewards.append(0)
				elif hand.hand_strength == self.dealer.hand_strength:
					player_rewards.append(hand.amount_betted_on_hand)
				elif hand.hand_strength > self.dealer.hand_strength:
					player_rewards.append(hand.amount_betted_on_hand * 2)
				else:
					player_rewards.append(hand.amount_betted_on_hand * 2)
			player.recieve_rewards([(player_hands[i], player_rewards[i]) for i in range(len(player_hands))], dealer_cards)

	def play(self, number_of_rounds: int = 100, print_rounds_progress: bool = False):
		next_milestone = 0
		for i in range(number_of_rounds):
			progress = (i / number_of_rounds) * 100
			self.total_rounds_played += 1
			if progress >= next_milestone:
				next_milestone += 10
				if print_rounds_progress:
					print(str(progress) + '% of the rounds were played.')
			# Shuffle according to the total number of rounds played
			if self.total_rounds_played % self.shuffle_every == 0:
				self.deck.shuffle_cards()
				self.card_count = 0
			# Requesting the initial bets from the players
			initial_bets = self.request_initial_bet_from_players()
			# Drawing the starting cards for the players and the dealer
			self.draw_round_cards(initial_bets)
			# Making the players play their turn until all of their hands have stood
			self.request_actions_from_players()
			# Making the dealer do his moves
			self.request_actions_from_dealer()
			# Ending the round by giving the due rewards to the players (if they won or drew)
			self.give_rewards()
			# Adding the cards of the deck back to the back of the deck
			self.deck.add_drawn_cards_back()
		if print_rounds_progress:
			print('DONE!')

	def play_same_conditions(self, number_of_rounds: int = 100): # Plays the players under the same conditions, ex. drawing same cards
		for i in range(number_of_rounds):
			self.total_rounds_played += 1
			# Shuffle according to the total number of rounds played
			if self.total_rounds_played % self.shuffle_every == 0:
				self.deck.shuffle_cards()
				self.card_count = 0
			# Requesting the initial bets from the players
			initial_bets = self.request_initial_bet_from_players()
			# Drawing the hand for each player and the dealer
			players_card_1 = self.draw_single_card()
			players_card_2 = self.draw_single_card()
			for player in self.players:
				player_hand = Hand(players_card_1, players_card_2, initial_bets[player])
				self.player_hands[player].overwrite_root(player_hand)
			self.dealer.start_new_turn(self.draw_single_card(), self.draw_single_card())
			# Requesting the actions from the players
			extra_drawn_cards = [] # This will be used so that the players draw the same cards
			for player in self.players:
				extra_drawn_cards_cpy = extra_drawn_cards.copy()
				next_hands = self.player_hands[player].get_tree_as_list()
				last_completed_hand = None
				# Keep on requesting the actions from the player for the given hand
				while len(next_hands) != 0:
					target_hand = next_hands[0]
					action = player.play_move(target_hand, self.dealer.up_card)
					# If the player decides to stand
					if action == 'S':
						# Let the current hand be completed and get all of the remaining hands after this hand
						last_completed_hand = target_hand
						next_hands = self.player_hands[player].get_all_hands_after_hand(target_hand)
					# If the player decides to split
					elif action == 'P':
						# Request the money to split from the player
						amount = player.force_amount_to_be_betted(target_hand.amount_betted_on_hand)
						# Build up the two hands which will replace the hand being splitted
						target_hand_card_1 = target_hand.cards[0]
						target_hand_card_2 = target_hand.cards[1]
						new_card_1 = None
						if len(extra_drawn_cards_cpy) > 0:
							new_card_1 = extra_drawn_cards_cpy.pop(0)
						else:
							new_card_1 = self.draw_single_card()
							extra_drawn_cards.append(new_card_1)
						new_card_2 = None
						if len(extra_drawn_cards_cpy) > 0:
							new_card_2 = extra_drawn_cards_cpy.pop(0)
						else:
							new_card_2 = self.draw_single_card()
							extra_drawn_cards.append(new_card_2)
						output_hand1 = Hand(target_hand_card_1, new_card_1, amount)
						output_hand2 = Hand(target_hand_card_2, new_card_2, amount)
						# Actually perform the replacement
						self.player_hands[player].replace(target_hand, output_hand1, output_hand2)
						# Always keep hands which are not yet completed in the list of hands that need to be evaluated
						if last_completed_hand != None:
							next_hands = self.player_hands[player].get_all_hands_after_hand(last_completed_hand)
						else:
							next_hands = self.player_hands[player].get_tree_as_list()
					# If the player decides to double down
					elif action == 'D':
						amount = player.force_amount_to_be_betted(target_hand.amount_betted_on_hand)
						target_hand.add_amount_to_bet(amount)
						new_card = None
						if len(extra_drawn_cards_cpy) > 0:
							new_card = extra_drawn_cards_cpy.pop(0)
						else:
							new_card = self.draw_single_card()
							extra_drawn_cards.append(new_card)
						target_hand.add_card(new_card)
						target_hand.has_doubled_down = True
					else:
						new_card = None
						if len(extra_drawn_cards_cpy) > 0:
							new_card = extra_drawn_cards_cpy.pop(0)
						else:
							new_card = self.draw_single_card()
							extra_drawn_cards.append(new_card)
						target_hand.add_card(new_card)
			# Making the dealer take his actions
			self.request_actions_from_dealer()
			# Ending the round
			self.give_rewards()
			# Adding the cards of the deck back
			self.deck.add_drawn_cards_back()



first_time = False

if __name__ == '__main__':
	# Starting the timer
	start_time = timeit.default_timer()

	# To set the subfolder name
	train_id = str(uuid.uuid4())

	# Params to test for
	learning_rates = [0.1, 0.01, 0.001]
	discount_factors = [0.7, 0.8, 0.9]
	exploration_rates = [0.05, 0.1, 0.2]

	# Number of games to be played for training
	num_training_games = 1000000
	# Number of games to be played for testing
	num_testing_games = 100000

	# The list of policies encompassing all of the combinations
	policies = list()
	# Populating the policies
	for learning_rate in learning_rates:
		for discount_factor in discount_factors:
			for exploration_rate in exploration_rates:
				policy = QLearningBlackjackPolicy(learning_rate, discount_factor, exploration_rate, train_id)
				policy.initial_save()
				policies.append(policy)

	print('Training ' + str(len(policies)) + ' policies...')

	# The game in which the q learning agents will be trained
	blackjack_game = Blackjack(
		[QLearningBasicStrategyLearningAgent(policy) for policy in policies],
		minimum_bet=1,
		maximum_bet=1,
		number_of_decks=8,
		shuffle_every=50
	)

	# Will be used when building the final graphs
	save_iteration_index = [0]
	# Running the game to train the algorithms
	for i in progressbar.progressbar(range(1, num_training_games + 1)):
		# Same conditions ideal so as to ensure same training conditions for each player
		blackjack_game.play_same_conditions(1)
		# Saving more often at the beginning of the training when the algorithm will learn fastest
		if (i <= 10000 and i % 1000 == 0):
			save_iteration_index.append(i)
			for policy in policies:
				policy.save_progress(i)
		elif (i <= 100000 and i % 10000 == 0):
			save_iteration_index.append(i)
			for policy in policies:
				policy.save_progress(i)
		elif (i % 100000 == 0):
			save_iteration_index.append(i)
			for policy in policies:
				policy.save_progress(i)

	# Calculating the time it took for the algorithm to finish
	elapsed_time = round((timeit.default_timer() - start_time)/60, 1)
	print('Training of ' + str(len(policies)) + ' policies took ' + str(elapsed_time) + 'mins.')

	# Loading the policies as static players, i.e. players that cannot learn any further so as to evaluate them
	# Each policy will be loaded for each save which occurred so as to see the progression in learning the game of blackjack
	static_player_loc = os.path.join(os.getcwd(), 'q_learning', train_id)
	static_players = list()
	for path in glob.glob(static_player_loc + '/*.json'):
		id = path.split('\\')[-1].split('.')[0].split('_')[-1]
		static_players.append(QLearningBlackjackPolicy.load_iterations_as_static_players(id, train_id, True))

	# For game playing reducing the static players list to 1 dimension
	reduced_dim_players = [player for (variation, _, _, _) in static_players for player in variation]

	# Creating the game in which the players will be tested 
	blackjack_testing_game = Blackjack(reduced_dim_players, 
		minimum_bet=1, 
		maximum_bet=1, 
		number_of_decks=8, 
		shuffle_every=50)
	# Playing the testing rounds
	print('Playing the testing rounds...')
	for i in progressbar.progressbar(range(1, num_testing_games + 1)):
		blackjack_testing_game.play_same_conditions(1)

	# To output the results as a csv and a prettytable
	output_table = {
		'learning_rate': list(),
		'discount_factor': list(),
		'exploration_rate': list(),
		'wins': list(),
		'losses': list(),
		'net_chips': list()
	}

	# Compiling the data for the following graphs
	wins, losses, net_money = list(), list(), list()
	for static_player in static_players:
		current_wins, current_losses, current_net_money = list(), list(), list()
		for progression in static_player[0]:
			current_wins.append(progression.num_matches_won)
			current_losses.append(progression.num_matches_lost)
			current_net_money.append(progression.chips)
		wins.append(current_wins)
		losses.append(current_losses)
		net_money.append(current_net_money)
		# Adding the data to the output table
		output_table['learning_rate'].append(static_player[1])
		output_table['discount_factor'].append(static_player[2])
		output_table['exploration_rate'].append(static_player[3])
		output_table['wins'].append(current_wins[-1])
		output_table['losses'].append(current_losses[-1])
		output_table['net_chips'].append(current_net_money[-1])

	output_dataframe = pd.DataFrame(output_table)
	output_dataframe.sort_values(['losses', 'wins', 'net_chips'], ascending=[True, False, False], inplace=True)
	output_dataframe.to_csv('q_learning-multiple_params.csv')
	print(output_dataframe)

	# Constructing the graphs to be outputted
	(fig, axs) = plt.subplots(1, 3)
	fig.set_size_inches(15, 4.8)

	# Plotting the data on the axis
	for i in range(len(wins)):
		curr_w, curr_l, curr_m = wins[i], losses[i], net_money[i]
		#color = ('#' + str(hex(random.randint(0, 255))).split('x')[-1] 
		#             + str(hex(random.randint(0, 255))).split('x')[-1]  
		#			 + str(hex(random.randint(0, 255))).split('x')[-1])
		[ _wins ] = axs[0].plot(
			save_iteration_index,
			curr_w,
			#color=color,
			linestyle='-',
			linewidth=1)
		[ _losses ] = axs[1].plot(
			save_iteration_index,
			curr_l,
			#color=color,
			linestyle='-',
			linewidth=1)
		[ _net_money ] = axs[2].plot(
			save_iteration_index,
			curr_m,
			#color=color,
			linestyle='-',
			linewidth=1)

	# Setting some axis params

	# Wins
	axs[0].set_xlim(0, max(save_iteration_index))
	axs[0].set_ylim(0, num_testing_games)
	axs[0].set_xlabel('Training games played')
	axs[0].set_ylabel('Wins')
	axs[0].grid(True)
	axs[0].set_title('Training Win Progression')
	#axs[0].legend()

	# Losses
	axs[1].set_xlim(0, max(save_iteration_index))
	axs[1].set_ylim(0, num_testing_games)
	axs[1].set_xlabel('Training games played')
	axs[1].set_ylabel('Losses')
	axs[1].grid(True)
	axs[1].set_title('Training Loss Progression')
	#axs[1].legend()

	# Losses
	axs[2].set_xlabel('Training games played')
	axs[2].set_ylabel('Net Chips')
	axs[2].grid(True)
	axs[2].set_title('Training Chips Progression')
	#axs[2].legend()

	fig.canvas.set_window_title('Training Progress')
	fig.tight_layout()
	fig.show()
	fig.savefig('training-progress-qlearning')

	pass
