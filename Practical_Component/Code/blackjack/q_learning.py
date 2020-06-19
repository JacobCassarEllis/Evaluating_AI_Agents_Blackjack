import sys, os
import numpy as np
import pickle
import json
from collections import namedtuple

Decision = namedtuple('Decision', ['state', 'action'], verbose=False)

class Episode:
	def __init__(self, initial_decisions: list = []):
		self.episode_decisions = [decision for decision in initial_decisions]

	def add_new_decision(self, decision: Decision):
		self.episode_decisions.append(decision)

	def spawn_two_episodes_from_self(self):
		episode_1 = Episode(self.episode_decisions)
		episode_2 = Episode(self.episode_decisions)
		return (episode_1, episode_2)

	def get_decisions_reversed(self):
		return self.episode_decisions[::-1]

	def get_current_and_next_decision_tuples(self):
		output = []
		previous = None
		for decision in self.episode_decisions:
			if previous != None:
				dual = (previous, decision)
				output.append(dual)
			previous = decision
		output.append((previous, None))
		return output


def get_initial_player_q_values():
	player_q_values = {}
	# When player has a hard and not splittable hand
	for i in range(4, 22): # All possible amounts in hand for the player for a hard hand 4-21
		for j in range(2, 12): # All possible dealer up card values 2-11
			player_q_values[(i, False, False, j)] = {}
			for action in ['H', 'S', 'D']: # No split due to the above assumption
				if action == 'H':
					player_q_values[(i, False, False, j)][action] = 1
				else:
					player_q_values[(i, False, False, j)][action] = 0
	# When player has a soft and not splittable hand
	for i in range(13, 22): # All possible amounts in hand for the player for a soft hand 13-21
		for j in range(2, 12): # All possible dealer up card values 1-11
			player_q_values[(i, True, False, j)] = {}
			for action in ['H', 'S', 'D']: # No split due to not splittable assumption
				if action == 'H':
					player_q_values[(i, True, False, j)][action] = 1
				else:
					player_q_values[(i, True, False, j)][action] = 0
	# Special Instance when we have a soft card available and hand is splittable
	for j in range(2, 12):
		player_q_values[(12, True, True, j)] = {} # We know strength of this hand is 12 since 11 + 1 = 12
		for action in ['H', 'S', 'D', 'P']:
			if action == 'P':
				player_q_values[(12, True, True, j)][action] = 1
			else:
				player_q_values[(12, True, True, j)][action] = 0
	# Regular splittable instance with no soft card
	for i in [4, 6, 8, 10, 12, 14, 16, 18, 20]: # When a hand is splittable, the total must be even
		for j in range(2, 12):
			player_q_values[(i, False, True, j)] = {}
			for action in ['H', 'S', 'D', 'P']:
				if action == 'S':
					player_q_values[(i, False, True, j)][action] = 1
				else:
					player_q_values[(i, False, True, j)][action] = 0
	return player_q_values

class QLearningBlackjackPolicy:
	def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.8, exploration_rate: float = 0.2, subfolder: str = None):
		self.id = str(uuid.uuid4())
		self.player_q_values = get_initial_player_q_values()
		self.learning_rate = learning_rate
		self.discount_factor = discount_factor
		self.exploration_rate = exploration_rate
		self.episode_list = [Episode()]
		self.current_episode_index = 0
		self.subfolder = subfolder
		cwd = os.getcwd()
		joined = os.path.join(cwd, 'q_learning', subfolder)
		exists = os.path.exists(joined)
		if subfolder != None and not exists:
			os.mkdir(joined)


	def get_greedy_decision(self, state):
		action = None
		action_value = -999999
		for a in self.player_q_values[state].keys():
			a_value = self.player_q_values[state][a]
			if a_value > action_value:
				action = a
				action_value = a_value
		return action

	def choose_next_action(self, state, possible_actions: list):
		# If we can only perform one action, there is no decision to be made so do it
		if len(possible_actions) == 1: return possible_actions[0]

		if np.random.uniform(0, 1) <= self.exploration_rate:
			# If we are exploring choose a random action from those available
			action = np.random.choice(possible_actions)
			return action
		else:
			# If we are not exploring always take the greedy approach
			return self.get_greedy_decision(state)

	def add_move_to_tree(self, state, action):
		# If no new moves should be added to the tree, simply exit from the function
		if self.current_episode_index == len(self.episode_list): return
		if action == 'P': # Split case
			current_episode = self.episode_list[self.current_episode_index]
			current_episode.add_new_decision(Decision(state, action))
			episode_1, episode_2 = current_episode.spawn_two_episodes_from_self()
			self.episode_list.remove(current_episode)
			self.episode_list.insert(self.current_episode_index, episode_1)
			self.episode_list.insert(self.current_episode_index + 1, episode_2)
		elif action == 'S': # Stand case
			# Only add it to the tree if total is <= 21, since we don't need to learn anything when we bust
			if state[0] <= 21:
				current_episode = self.episode_list[self.current_episode_index]
				current_episode.add_new_decision(Decision(state, action))
			self.current_episode_index += 1
		else: # Hit / Double down case
			current_episode = self.episode_list[self.current_episode_index]
			current_episode.add_new_decision(Decision(state, action))

	def give_credit(self, rewards_list: list):
		# Rewards list should correspond to the reward for each episode in the episode list
		for i in range(len(self.episode_list)):
			# This iteration's episode
			episode = self.episode_list[i]
			j = 1
			for (current, next) in episode.get_current_and_next_decision_tuples():
				# Unpacking the current decision
				(current_state, current_action) = current
				# Calculating the reward for this action
				current_reward = rewards_list[i] * (2 if current_action == 'D' else 1)
				# The current reward for this state-action pair
				old_value = self.player_q_values[current_state][current_action]
				# By the equation gamma ^ time
				discount = self.discount_factor ** j
				# Applying the learning algorithm -- CHECK THIS OUT
				if next == None:
					derived_reward = old_value + self.learning_rate * (current_reward + (discount * 0) - old_value)
				else:
					# Unpacking the next decision to get the next state
					(next_state, _) = next
					# Getting the maximum reward for the next state
					max_next = max(self.player_q_values[next_state].values())
					# Using it to learn the value of this state-action pair
					derived_reward = old_value + self.learning_rate * (current_reward + (discount * max_next) - old_value)
				rounded = round(derived_reward, 3)
				# Updating the reward in the q table for this action
				self.player_q_values[current_state][current_action] = rounded
				j += 1
		self.episode_list = [Episode()]
		self.current_episode_index = 0
		
	def export_training_as_csv(self, filename: str):
		lines = []
		for i in range(4, 22):
			line = []
			for j in range(2, 12):
				action = self.get_greedy_decision((i, False, False, j))
				line.append(action)
			lines.append(','.join(line))
		for i in range(13, 22):
			line = []
			for j in range(2, 12):
				action = self.get_greedy_decision((i, True, False, j))
				line.append(action)
			lines.append(','.join(line))
		line = []
		for j in range(2, 12):
			action = self.get_greedy_decision((12, True, True, j))
			line.append(action)
		lines.append(','.join(line))
		for i in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
			line = []
			for j in range(2, 12):
				action = self.get_greedy_decision((i, False, True, j))
				line.append(action)
			lines.append(','.join(line))
		output_csv = '\n'.join(lines)
		with open(filename, 'w') as file:
			file.write(output_csv)

	def print_rewards(self):
		output = []
		for (key, value) in self.player_q_values.items():
			item = {
				'key': {
					'hand_strength': key[0],
					'has_soft': key[1],
					'can_split': key[2],
					'dealer_up_strength': key[3]
				},
				'action_values': value
			}
			output.append(item)
		print(json.dumps(output, indent=3))

	def convert_q_table_to_jsonable(self):
		output = []
		for (hand_strength, has_soft, splittable, dealer_up), actions in self.player_q_values.items():
			output.append({
				"key": {
					"hand_strength": hand_strength,
					"has_soft": has_soft,
					"splittable": splittable,
					"dealer_up": dealer_up
				},
				"actions": actions
			})
		return output

	def initial_save(self):
		properties = {
			"id": self.id,
			"learning_rate": self.learning_rate,
			"discount_factor": self.discount_factor,
			"exploration_rate": self.exploration_rate,
			"progress_saves": [
				{
					"q_values": self.convert_q_table_to_jsonable(),
					"csv_string": self.to_csv_string(),
					"num_iterations": 0
				}
			]
		}
		file_loc = 'q_learning/' + ((self.subfolder + '/ql_' + self.id + '.json') if self.subfolder!=None else ('ql_' + self.id + '.json'))
		with open(file_loc, 'w') as file:
			file.write(json.dumps(properties))

	def save_progress(self, num_iterations):
		file_loc = 'q_learning/' + ((self.subfolder + '/ql_' + self.id + '.json') if self.subfolder!=None else ('ql_' + self.id + '.json'))
		with open(file_loc, 'r') as file:
			properties = json.loads(file.read())
		properties['progress_saves'].append({ 
			"q_values": self.convert_q_table_to_jsonable(),
			"csv_string": self.to_csv_string(),
			"num_iterations": num_iterations
		})
		with open(file_loc, 'w') as file:
			file.write(json.dumps(properties))

	@staticmethod
	def load(location: str = 'qlearningprogress.pickle'):
		with open(location, 'rb') as file:
			q_learning = pickle.load(file)
		return q_learning

	@staticmethod
	def load(ql_id: str, subfolder:str=None):
		file_loc = 'q_learning/' + ((subfolder + '/ql_' + ql_id + '.json') if subfolder!=None else ('ql_' + self.id + '.json'))
		with open(file_loc, 'r') as file:
			properties = json.loads(file.read())
		id = properties['id']
		learning_rate = properties['learning_rate']
		discount_factor = properties['discount_factor']
		exploration_rate = properties['exploration_rate']
		policy = QLearningBlackjackPolicy(learning_rate, discount_factor, exploration_rate)
		policy.id = id
		policy.player_q_values = convert_jsonable_to_q_table(properties['progress_saves'][-1]['q_values'])
		return policy

	@staticmethod
	def load_iterations_as_static_players(ql_id: str, subfolder:str=None, output_params:bool=False):
		file_loc = 'q_learning/' + ((subfolder + '/ql_' + ql_id + '.json') if subfolder!=None else ('ql_' + self.id + '.json'))
		with open(file_loc, 'r') as file:
			properties = json.loads(file.read())
		output_players = []
		for progress_save in properties['progress_saves']:
			output_players.append(StringLoadedPlayer(progress_save['csv_string'], 0))
		if not output_params: 
			return output_players
		else:
			return (output_players, properties['learning_rate'], properties['discount_factor'], properties['exploration_rate'])

class QLearningBasicStrategyLearningAgent(PlayerConcept):
	def __init__(self, policy: QLearningBlackjackPolicy):
		super().__init__(0)
		self.policy = policy

	def place_initial_bet(self, minimum_bet: int, maximum_bet: int, count):
		return minimum_bet # We are not using the chips variable because we want an infinite amount
				           # of chips for training

	def get_greedy_decision(self, state):
		action = None
		action_value = -999999
		for a in self.player_q_values[state].keys():
			a_value = self.player_q_values[state][a]
			if a_value > action_value:
				action = a
				action_value = a_value
		return action

	def choose_next_action(self, state, possible_actions: list):
		# If we can only perform one action, there is no decision to be made so do it
		if len(possible_actions) == 1: return possible_actions[0]

		if np.random.uniform(0, 1) <= self.exploration_rate:
			# If we are exploring choose a random action from those available
			action = np.random.choice(possible_actions)
			return action
		else:
			# If we are not exploring always take the greedy approach
			return self.get_greedy_decision(state)