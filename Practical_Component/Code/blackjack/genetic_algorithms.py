import sys, os
import numpy as np
import uuid
import json
import threading
from random import *
from blackjack import *
from player import *

class Chromosome(PlayerConcept):
	def __init__(self, moves: tuple = None):
		super().__init__(0)
		if moves != None:
			(hard, soft, special, splittable) = moves
			self.hard = hard
			self.soft = soft
			self.special = special
			self.splittable = splittable
		else:
			self.hard = {}
			hard_moves = ['S', 'H', 'D']
			for i in range(4, 22):
				for j in range(2, 12):
					self.hard[(i, False, False, j)] = Chromosome.get_random_move(hard_moves)
			self.soft = {}
			soft_moves = ['S', 'H', 'D']
			for i in range(13, 22):
				for j in range(2, 12):
					self.soft[(i, True, False, j)] = Chromosome.get_random_move(soft_moves)
			splittable_moves = ['S', 'H', 'D', 'P']
			self.special = {}
			for j in range(2, 12):
				self.special[(12, True, True, j)] = Chromosome.get_random_move(splittable_moves)
			self.splittable = {}
			for i in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
				for j in range(2, 12):
					self.splittable[(i, False, True, j)] = Chromosome.get_random_move(splittable_moves)

	def is_equal_to(self, other):
		if type(self) != type(other): return False
		if self.hard != other.hard: return False
		if self.soft != other.soft: return False
		if self.special != other.special: return False
		if self.splittable != other.splittable: return False
		return True

	def mutate(self, mutation_prob):
		for i in range(4, 22):
			for j in range(2, 12):
				if np.random.uniform(0, 1) <= mutation_prob:
					current_value = self.hard[(i, False, False, j)]
					candidate_actions = ['S', 'H', 'D']
					candidate_actions.remove(current_value)
					self.hard[(i, False, False, j)] = Chromosome.get_random_move(candidate_actions)
		for i in range(13, 22):
			for j in range(2, 12):
				if np.random.uniform(0, 1) <= mutation_prob:
					current_value = self.soft[(i, True, False, j)]
					candidate_actions = ['S', 'H', 'D']
					candidate_actions.remove(current_value)
					self.soft[(i, True, False, j)] = Chromosome.get_random_move(candidate_actions)
		for j in range(2, 12):
			if np.random.uniform(0, 1) <= mutation_prob:
				current_value = self.special[(12, True, True, j)]
				candidate_actions = ['S', 'H', 'D', 'P']
				candidate_actions.remove(current_value)
				self.special[(12, True, True, j)] = Chromosome.get_random_move(candidate_actions)
		for i in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
			for j in range(2, 12):
				if np.random.uniform(0, 1) <= mutation_prob:
					current_value = self.splittable[(i, False, True, j)]
					candidate_actions = ['S', 'H', 'D', 'P']
					candidate_actions.remove(current_value)
					self.splittable[(i, False, True, j)] = Chromosome.get_random_move(candidate_actions)

	def place_initial_bet(self, minimum_bet: int, maximum_bet: int, count):
		self.chips -= minimum_bet
		return minimum_bet

	def play_move(self, hand: Hand, dealer_up_card):
		hand_strength = hand.hand_strength
		if hand_strength > 21: return 'S'
		is_soft = hand.has_soft_card_available()
		splittable = hand.can_split
		dealer_strength = dealer_up_card.value
		if is_soft and splittable:
			return self.special[(hand_strength, is_soft, splittable, dealer_strength)]
		elif is_soft and not splittable:
			return self.soft[(hand_strength, is_soft, splittable, dealer_strength)]
		elif not is_soft and splittable:
			return self.splittable[(hand_strength, is_soft, splittable, dealer_strength)]
		else:
			return self.hard[(hand_strength, is_soft, splittable, dealer_strength)]

	def recieve_rewards(self, rewards: list, dealer_cards: list):
		super().recieve_rewards(rewards, dealer_cards)
		for (hand, reward) in rewards:
			self.chips += reward

	def to_csv_string(self):
		lines = []
		for i in range(4, 22):
			line = []
			for j in range(2, 12):
				line.append(self.hard[(i, False, False, j)])
			lines.append(",".join(line))
		for i in range(13, 22):
			line = []
			for j in range(2, 12):
				line.append(self.soft[(i, True, False, j)])
			lines.append(",".join(line))
		line = []
		for j in range(2, 12):
			line.append(self.special[(12, True, True, j)])
		lines.append(",".join(line))
		for i in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
			line = []
			for j in range(2, 12):
				line.append(self.splittable[(i, False, True, j)])
			lines.append(",".join(line))
		return "\n".join(lines)

	@staticmethod
	def get_random_move(possible_moves: list = ['S']):
		if len(possible_moves) == 1: return possible_moves[0]
		else: return np.random.choice(possible_moves)

	@staticmethod
	def perform_chromosome_crossover(chromosome_1, chromosome_2, crossover_prob: float = 0.5):
		hard_1, hard_2 = {}, {}
		soft_1, soft_2 = {}, {}
		special_1, special_2 = {}, {}
		splittable_1, splittable_2 = {}, {}
		for i in range(4, 22):
			for j in range(2, 12):
				key = (i, False, False, j)
				if np.random.uniform(0, 1) >= crossover_prob: # Perform crossover
					hard_1[key] = chromosome_2.hard[key]
					hard_2[key] = chromosome_1.hard[key]
				else:
					hard_1[key] = chromosome_1.hard[key]
					hard_2[key] = chromosome_2.hard[key]
		for i in range(13, 22):
			for j in range(2, 12):
				key = (i, True, False, j)
				if np.random.uniform(0, 1) >= crossover_prob:
					soft_1[key] = chromosome_2.soft[key]
					soft_2[key] = chromosome_1.soft[key]
				else:
					soft_1[key] = chromosome_1.soft[key]
					soft_2[key] = chromosome_2.soft[key]
		for j in range(2, 12):
			key = (12, True, True, j)
			if np.random.uniform(0, 1) >= crossover_prob:
				special_1[key] = chromosome_2.special[key]
				special_2[key] = chromosome_1.special[key]
			else:
				special_1[key] = chromosome_1.special[key]
				special_2[key] = chromosome_2.special[key]
		for i in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
			for j in range(2, 12):
				key = (i, False, True, j)
				if np.random.uniform(0, 1) >= crossover_prob:
					splittable_1[key] = chromosome_2.splittable[key]
					splittable_2[key] = chromosome_1.splittable[key]
				else:
					splittable_1[key] = chromosome_1.splittable[key]
					splittable_2[key] = chromosome_2.splittable[key]
		genes_1 = (hard_1, soft_1, special_1, splittable_1)
		genes_2 = (hard_2, soft_2, special_2, splittable_2)
		child_1 = Chromosome(genes_1)
		child_2 = Chromosome(genes_2)
		return (child_1, child_2)
				
class GeneticAlgorithm:
	def __init__(self, population_size: int = 250, crossover_prob: float = 1.0, mutation_prob: float = 0.1, fitness_rounds: int = 10000, selection_mode: str = 'rank', tournament_size: int = 5):
		self.id = str(uuid.uuid4()) # So that we can individually identify each genetic algorithm we run
		self.generation_number = 0
		self.population_size = population_size
		self.crossover_prob = crossover_prob
		self.mutation_prob = mutation_prob
		self.fitness_rounds = fitness_rounds
		self.population = []
		self.crossover_method = selection_mode
		for i in range(self.population_size):
			self.population.append(Chromosome())
		self.fitnesses = self.get_population_fitness()
		if selection_mode == 'rank':
			self.perform_selection = self.perform_rank_selection
		elif selection_mode == 'roulette':
			self.perform_selection = self.perform_roulette_wheel_selection
		else:
			self.perform_selection = self.perform_tournament_selection
			self.tournament_size = tournament_size
		self.print_generation_details()
		self.initial_save()

	def get_population_fitness(self):
		testing_game = Blackjack(self.population)
		testing_game.play_same_conditions(self.fitness_rounds)
		fitnesses = []
		for chromosome in self.population:
			individual_fitness = (chromosome, chromosome.chips) # To help players differentiate between hit and double - more chips = better playing
			fitnesses.append(individual_fitness)
		return sorted(fitnesses, key=lambda x: x[1], reverse=True)

	def perform_rank_selection(self, fitnesses: list):
		ranks = []
		counter = 0
		# Getting the individuals ranked
		for individual_fitness in reversed(fitnesses):
			counter += 1
			ranks.append((individual_fitness[0], counter))
		shuffle(ranks)
		sum_ranks = sum([rank[1] for rank in ranks])
		parents = []
		# Selecting the parent pairs
		for i in range(int(self.population_size / 2)): # We will assume that the parents will always two children
			parent_1 = None
			parent_2 = None
			for i in range(2):
				generated = randint(0, sum_ranks)
				cumulative = 0
				for (chromosome, rank) in ranks:
					cumulative += rank
					if cumulative >= generated:
						if parent_1 == None:
							parent_1 = chromosome
							break
						else:
							if chromosome != parent_1:
								parent_2 = chromosome
								break
							elif chromosome == ranks[-1][0]:
								parent_2 = ranks[-2][0]
			parents.append((parent_1, parent_2))
		# Return the selected parent combinations
		return parents

	def perform_roulette_wheel_selection(self, fitnesses):
		total_fitness = sum([ fitness for (_, fitness) in fitnesses ])
		normalized_fitnesses = [ (individual, fitness / total_fitness) for (individual, fitness) in fitnesses ]
		shuffle(normalized_fitnesses)
		parents = []
		for i in range(int(self.population_size / 2)):
			parent_1 = None
			parent_2 = None
			for i in range(2):
				generated = np.random.uniform(0, 1)
				cumulative = 0
				for (chromosome, normalized_fitness) in normalized_fitnesses:
					cumulative += normalized_fitness
					if cumulative >= generated:
						if parent_1 == None:
							parent_1 = chromosome
							break
						else:
							if chromosome != parent_1:
								parent_2 = chromosome
								break
							elif chromosome == normalized_fitnesses[-1][0]:
								parent_2 = normalized_fitness[-2][0]
			parents.append((parent_1, parent_2))
		return parents

	def perform_tournament_selection(self, fitnesses):
		parents = list()
		for i in range(int(self.population_size / 2)):
			fitnesses_cpy = fitnesses.copy()
			current_parents = list()
			for i in range(2):
				# No need to actually build a tournament - just pick the best from the first k chosen
				selected = None
				for j in range(self.tournament_size):
					index = randint(0, len(fitnesses_cpy) - 1)
					popped = fitnesses_cpy.pop(index)
					if selected == None: 
						selected = popped
					elif selected[1] < popped[1]: 
						selected = popped
				current_parents.append(selected[0])
			parents.append((current_parents[0], current_parents[1]))
		return parents		

	def perform_crossover(self, parents):
		output_children = []
		for (parent_1, parent_2) in parents:
			(child_1, child_2) = Chromosome.perform_chromosome_crossover(parent_1, parent_2)
			child_1.mutate(self.mutation_prob)
			child_2.mutate(self.mutation_prob)
			output_children.extend([child_1, child_2])
		return output_children

	def execute_generation(self):
		print('Selecting the pairs of parents for the generation...')
		parents = self.perform_selection(self.fitnesses)
		print('Performing crossover and mutation to produce the population of the new generation...')
		children = self.perform_crossover(parents)
		self.population = children
		print('Calculating the fitness of the current generation...')
		self.fitnesses = self.get_population_fitness()
		print('Setting the index of the current generation...')
		self.generation_number += 1
		print('Saving the data about the best chromosome in the new generation...')
		self.save_best_chromosome()
		print('Done.')

	def learn(self, num_generations = 25):
		for i in range(num_generations):
			self.execute_generation()
			self.print_generation_details()

	def learn_until_convergance(self):
		gens_since_change_in_most_fit_chromosome = 0
		previous_most_fit = self.fitnesses[0][0]
		while gens_since_change_in_most_fit_chromosome < 25:
			self.execute_generation()
			self.print_generation_details()
			current_most_fit = self.fitnesses[0][0]
			if current_most_fit.is_equal_to(previous_most_fit):
				gens_since_change_in_most_fit_chromosome += 1
			else:
				gens_since_change_in_most_fit_chromosome = 0
				previous_most_fit = current_most_fit

	def print_generation_details(self):
		total_fitness = sum([individual_fitness[1] for individual_fitness in self.fitnesses])
		print("Algorithm ID: " + str(self.id))
		print("Generation Number:" + str(self.generation_number))
		print("Best Chromosome Fitness: " + str(self.fitnesses[0][1])) 
		print("Average Fitness: " + str(total_fitness / self.population_size))
		print("Total Fitness: " + str(total_fitness))
		print("Best Individual:")
		print(self.fitnesses[0][0].to_csv_string(), end='\n\n')
	
	def initial_save(self):
		properties = {
			"id": self.id,
			"population_size": self.population_size,
			"crossover_prob": self.crossover_prob,
			"mutation_prob": self.mutation_prob,
			"fitness_rounds": self.fitness_rounds,
			"crossover_method": self.crossover_method,
			"generational_best_individuals": [ 
				{ 
					"entries": {
						"hard": [ { "key": key, "value": value } for (key, value) in self.fitnesses[0][0].hard.items()],
						"soft": [ { "key": key, "value": value } for (key, value) in self.fitnesses[0][0].soft.items()],
						"special": [ { "key": key, "value": value } for (key, value) in self.fitnesses[0][0].special.items()],
						"splittable": [ { "key": key, "value": value } for (key, value) in self.fitnesses[0][0].splittable.items()]
					},
					"generation_number": self.generation_number,
					"fitness": self.fitnesses[0][1],
					"average_generation_fitness": sum([individual_fitness[1] for individual_fitness in self.fitnesses]) / self.population_size,
					"csv_string": self.fitnesses[0][0].to_csv_string()
				}
			]
		}
		if self.crossover_method == 'tournament':
			properties['tournament_size'] = self.tournament_size
		with open('genetic_algorithm/ga_' + self.id + '.json', 'w') as file:
			file.write(json.dumps(properties))
		
	def save_best_chromosome(self):
		with open('genetic_algorithm/ga_' + self.id + '.json', 'r') as file:
			properties = json.loads(file.read())
		properties['generational_best_individuals'].append({ 
			"entries": {
				"hard": [ { "key": key, "value": value } for (key, value) in self.fitnesses[0][0].hard.items()],
				"soft": [ { "key": key, "value": value } for (key, value) in self.fitnesses[0][0].soft.items()],
				"special": [ { "key": key, "value": value } for (key, value) in self.fitnesses[0][0].special.items()],
				"splittable": [ { "key": key, "value": value } for (key, value) in self.fitnesses[0][0].splittable.items()]
			},
			"generation_number": self.generation_number,
			"fitness": self.fitnesses[0][1],
			"average_generation_fitness": sum([individual_fitness[1] for individual_fitness in self.fitnesses]) / self.population_size,
			"csv_string": self.fitnesses[0][0].to_csv_string()
		})
		with open('genetic_algorithm/ga_' + self.id + '.json', 'w') as file:
			file.write(json.dumps(properties))

	@staticmethod
	def load_best_chromosome_of_each_generation(ga_id: str):
		with open('genetic_algorithm/ga_' + ga_id + '.json', 'r') as file:
			json_obj = json.loads(file.read())
		output_chromosomes = []
		for chromosome in json_obj['generational_best_individuals']:
			csv_string = chromosome['csv_string']
			fitness = chromosome['fitness']
			average_fitness = chromosome['average_generation_fitness'] if ('average_generation_fitness' in chromosome) else None
			generation_number = chromosome['generation_number'] if ('generation_number' in chromosome) else None
			output_chromosomes.append((StringLoadedPlayer(csv_string, 0), fitness, average_fitness, generation_number))
		return (output_chromosomes, 
				json_obj['population_size'], 
				json_obj['crossover_prob'], 
				json_obj['mutation_prob'], 
				json_obj['fitness_rounds'], 
				json_obj['crossover_method'],
				(json_obj['tournament_size'] if 'tournament_size' in json_obj else None))

if __name__ == '__main__':
	ga1 = GeneticAlgorithm(300, 0.5, 0.005, 10000, 'roulette', 3)
	ga2 = GeneticAlgorithm(300, 0.5, 0.01, 10000, 'roulette', 3)
	ga3 = GeneticAlgorithm(400, 0.5, 0.005, 10000, 'roulette', 3)
	ga4 = GeneticAlgorithm(400, 0.5, 0.01, 10000, 'roulette', 3)

	t1 = threading.Thread(target=ga1.learn, args=(200,))
	t2 = threading.Thread(target=ga2.learn, args=(200,))
	t3 = threading.Thread(target=ga3.learn, args=(200,))
	t4 = threading.Thread(target=ga4.learn, args=(200,))

	t1.start()
	t2.start()
	t3.start()
	t4.start()

	t1.join()
	t2.join()
	t3.join()
	t4.join()

	print('Done training 3 GAs!')

	pass