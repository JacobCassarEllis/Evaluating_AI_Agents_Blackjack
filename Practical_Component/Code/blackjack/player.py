import sys, os
import numpy as np
from blackjack import *
from NeuralNet_blackjack.Player import *
from NeuralNet_blackjack.blackjack import *
from NeuralNet_blackjack.actions import *

class PlayerConcept:
	def __init__(self, chips: int):
		self.chips = chips 
		self.num_matches_won = 0
		self.num_matches_drawn = 0
		self.num_matches_lost = 0

	def place_initial_bet(self, minimum_bet: int, maximum_bet: int, count): # This should be learnt when card counting
		pass

	def force_amount_to_be_betted(self, amount: int):
		self.chips -= amount
		return amount

	def play_move(self, hand, dealer_up_card): # This should be learnt - optimal solution is blackjack basic strategy
		pass

	def recieve_rewards(self, rewards: list, dealer_cards: list):
		# So that we can easily analyze how two players perform when playing blackjack
		for (hand, reward) in rewards:
			if hand.amount_betted_on_hand > reward:
				self.num_matches_lost += 1
			elif hand.amount_betted_on_hand == reward:
				self.num_matches_drawn += 1
			elif hand.amount_betted_on_hand < reward:
				self.num_matches_won += 1

	def remove_impossible_gameplay_options(self, options: list, betted_amount):
		# Removes the split or double down options (if they are available) if
		# the user does not have enough chips to choose them
		if betted_amount > self.chips:
			if 'P' in options:
				options.remove('P')
			if 'D' in options:
				options.remove('D')
		return options

class HumanPlayer(PlayerConcept):
	def __init__(self, amount_of_chips):
		super().__init__(amount_of_chips)

	def place_initial_bet(self, minimum_bet: int, maximum_bet: int, count):
		while True:
			print('\nYou have ' + str(self.chips) + ' chips available.')
			print('Please enter an amount between ' + str(minimum_bet) + ' and ' + str(maximum_bet) + ' you want to bet.')
			amount = int(input())
			if amount >= minimum_bet and amount <= maximum_bet and amount <= self.chips:
				print('You have betted ' + str(amount) + ' chips on this hand.')
				self.chips -= amount
				return amount
			else:
				print('You have entered an invalid amount!')

	def play_move(self, hand, dealer_up_card):
		print('\nYour hand consists of the following faces:')
		for card in hand.cards:
			print(card.face + ' of ' + card.suit)
		if hand.hand_strength == 21:
			print('BLACKJACK! You have a hand strength of 21!')
			return 'S'
		elif hand.hand_strength > 21:
			print('BUST! Your hand strength exceeded 21.')
			return 'S'
		while True:
			print('You can play any of the following moves:')
			hand_moves = hand.get_possible_moves()
			possible_moves = self.remove_impossible_gameplay_options(hand_moves, hand.amount_betted_on_hand)
			print(', '.join(possible_moves))
			print('Enter the letter of the move you want to play:')
			action = input()
			if action in possible_moves:
				print('Move recorded!')
				return action
			else:
				print('Choice is invalid!')

	def recieve_rewards(self, rewards, dealer_cards: list):
		super().recieve_rewards(rewards, dealer_cards)
		print('\nDealer cards:')
		print('\n'.join([card.face + ' ' + card.suit for card in dealer_cards]))
		for (hand, reward) in rewards:
			print('\nYour hand:')
			print('\n'.join([card.face + ' ' + card.suit for card in hand.cards]))
			if hand.amount_betted_on_hand > reward:
				print('You LOST this hand.')
			elif hand.amount_betted_on_hand == reward:
				print('You DREW this hand.')
			elif hand.amount_betted_on_hand < reward:
				print('You WON this hand.')
			self.chips += reward
			print('Your new chip stack total is: ' + str(self.chips))

class QLearningBasicStrategyLearningAgent(PlayerConcept):
	def __init__(self, policy: QLearningBlackjackPolicy):
		super().__init__(0)
		self.policy = policy

	def place_initial_bet(self, minimum_bet: int, maximum_bet: int, count):
		return minimum_bet # We are not using the chips variable because we want an infinite amount
# of chips for training

	def play_move(self, hand, dealer_up_card):
		# Building the current state tuple
		current_state = (hand.hand_strength, hand.has_soft_card_available(), hand.can_split, dealer_up_card.value)
		# Getting the action to be performed for this current state
		# NOT CHECKING IF MOVE CAN BE DONE DUE TO CHIPS SINCE WE DON'T CARE ABOUT CHIPS
		action = self.policy.choose_next_action(current_state, hand.get_possible_moves())
		# Recording the combination so that it may be rewarded
		self.policy.add_move_to_tree(current_state, action)
		# Returning the action
		return action

	def recieve_rewards(self, rewards: list, dealer_cards: list):
		super().recieve_rewards(rewards, dealer_cards)

		# Receives a list of rewards whereby each reward corresponds to a hand the player had

		# They are not being added to the stack of chips as we do not care for that for training
		# We only care about its effect on the training of the Q learning algorithm

		policy_credit = []
		for (hand, reward) in rewards:
			if reward < hand.amount_betted_on_hand:
				policy_credit.append(-1)
			elif reward == hand.amount_betted_on_hand:
				policy_credit.append(0)
			else:
				policy_credit.append(1)

		self.policy.give_credit(policy_credit)

class BaselinePlayer(PlayerConcept): 
	def __init__(self, amount_of_chips: int):
		super().__init__(amount_of_chips)

	def place_initial_bet(self, minimum_bet: int, maximum_bet: int, count):
		self.chips -= minimum_bet
		return minimum_bet # We are not using the chips variable because we want an infinite amount
				           # of chips for training

	def play_move(self, hand, dealer_up_card):
		pass

	def recieve_rewards(self, rewards: list, dealer_cards: list):
		super().recieve_rewards(rewards, dealer_cards)
		for (hand, reward) in rewards:
			self.chips += reward

class NeverBustPlayer(BaselinePlayer): # The never bust strategy
	def __init__(self, amount_of_chips: int):
		super().__init__(amount_of_chips)

	def play_move(self, hand, dealer_up_card):
		if hand.hand_strength >= 12:
			return 'S'
		else:
			return 'H'

class MimickTheDealerPlayer(BaselinePlayer): # The mimick the dealer strategy
	def __init__(self, amount_of_chips: int):
		super().__init__(amount_of_chips)

	def play_move(self, hand, dealer_up_card):
		if hand.hand_strength < 17 or (hand.hand_strength == 17 and hand.has_soft_card_available()):
			return 'H'
		else:
			return 'S'

class RandomPlayer(BaselinePlayer): # The random move strategy
	def __init__(self, amount_of_chips: int):
		super().__init__(amount_of_chips)

	def play_move(self, hand, dealer_up_card):
		possible_moves = hand.get_possible_moves()
		possible_moves = self.remove_impossible_gameplay_options(possible_moves, hand.amount_betted_on_hand)
		return np.random.choice(possible_moves)

class LoadedPlayer(PlayerConcept):
	def __init__(self, training_location: str, amount_of_chips: int):
		super().__init__(amount_of_chips)
		self.strategy = {}
		with open(training_location, 'r') as file:
			text = file.read()
		lines = text.split('\n')
		current_line_index = 0
		for i in range(4, 22):
			current_line = lines[current_line_index]
			moves = current_line.split(',')
			current_action_index = 0
			for j in range(2, 12):
				self.strategy[(i, False, False, j)] = moves[current_action_index]
				current_action_index += 1
			current_line_index += 1
		for i in range(13, 22):
			current_line = lines[current_line_index]
			moves = current_line.split(',')
			current_action_index = 0
			for j in range(2, 12):
				self.strategy[(i, True, False, j)] = moves[current_action_index]
				current_action_index += 1
			current_line_index += 1
		current_line = lines[current_line_index]
		moves = current_line.split(',')
		current_action_index = 0
		for j in range(2, 12):
			self.strategy[(12, True, True, j)] = moves[current_action_index]
			current_action_index += 1
		current_line_index += 1
		for i in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
			current_line = lines[current_line_index]
			moves = current_line.split(',')
			current_action_index = 0
			for j in range(2, 12):
				self.strategy[(i, False, True, j)] = moves[current_action_index]
				current_action_index += 1
			current_line_index += 1

	def place_initial_bet(self, minimum_bet: int, maximum_bet: int, count):
		self.chips -= minimum_bet
		return minimum_bet # We are not using the chips variable because we want an infinite amount
				           # of chips for training

	def play_move(self, hand, dealer_up_card):
		if hand.hand_strength >= 21: return 'S'

		allowed_moves = hand.get_possible_moves()

		current_state = (hand.hand_strength, hand.has_soft_card_available(), hand.can_split, dealer_up_card.value)
		action = self.strategy[current_state] # Greedy -- no exploration

		if action not in allowed_moves:
			if action == 'D': action = 'H'
			elif action == 'P': action = 'S'

		return action

	def recieve_rewards(self, rewards: list, dealer_cards: list):
		super().recieve_rewards(rewards, dealer_cards)
		for (hand, reward) in rewards:
			self.chips += reward

class StringLoadedPlayer(PlayerConcept):
	def __init__(self, csv_string: str, amount_of_chips: int):
		super().__init__(amount_of_chips)
		self.strategy = {}
		lines = csv_string.split('\n')
		current_line_index = 0
		for i in range(4, 22):
			current_line = lines[current_line_index]
			moves = current_line.split(',')
			current_action_index = 0
			for j in range(2, 12):
				self.strategy[(i, False, False, j)] = moves[current_action_index]
				current_action_index += 1
			current_line_index += 1
		for i in range(13, 22):
			current_line = lines[current_line_index]
			moves = current_line.split(',')
			current_action_index = 0
			for j in range(2, 12):
				self.strategy[(i, True, False, j)] = moves[current_action_index]
				current_action_index += 1
			current_line_index += 1
		current_line = lines[current_line_index]
		moves = current_line.split(',')
		current_action_index = 0
		for j in range(2, 12):
			self.strategy[(12, True, True, j)] = moves[current_action_index]
			current_action_index += 1
		current_line_index += 1
		for i in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
			current_line = lines[current_line_index]
			moves = current_line.split(',')
			current_action_index = 0
			for j in range(2, 12):
				self.strategy[(i, False, True, j)] = moves[current_action_index]
				current_action_index += 1
			current_line_index += 1

	def place_initial_bet(self, minimum_bet: int, maximum_bet: int, count):
		self.chips -= minimum_bet
		return minimum_bet # We are not using the chips variable because we want an infinite amount
				           # of chips for training

	def play_move(self, hand, dealer_up_card):
		if hand.hand_strength >= 21: return 'S'

		allowed_moves = hand.get_possible_moves()

		current_state = (hand.hand_strength, hand.has_soft_card_available(), hand.can_split, dealer_up_card.value)
		action = self.strategy[current_state] # Greedy -- no exploration
		
		if action not in allowed_moves:
			if action == 'D': action = 'H'
			elif action == 'P': action = 'S'
		
		return action

	def recieve_rewards(self, rewards: list, dealer_cards: list):
		super().recieve_rewards(rewards, dealer_cards)
		for (hand, reward) in rewards:
			self.chips += reward
