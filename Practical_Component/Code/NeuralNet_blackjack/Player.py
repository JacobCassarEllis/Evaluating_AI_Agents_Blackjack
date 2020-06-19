import math
import random
import random as rand
import numpy as np

from blackjack import game
from tree import *
from blackjack import *
from actions import *
MAX =0
strategyMain = [['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
]
#states = []

# this class is for a Player of blackjack. A player has a name (string), a deck of cards, a bank to bet money
# along with total wins and total games player
# the player can be human or neural network (using my Simplex library)
class Player:
    def __init__(self, name, bank=1000, chips=1000, wins=0, games=0, network=None, policy=QLearningBlackjackPolicy()):
        self.dealers_amount = []
        self.playersAmount = []
        self.softOrHard = [] #true = soft , false = hard
        self.splittable = [] #last value card
        self.card_values = []
        self.initial_amount = bank
        self.name = name
        self.hand = Deck()
        self.amountBetted = 0
        self.handClass = None
        self.bank = bank
        self.wins = wins
        self.games = games
        self.network = network
        self.chips = chips
        self.num_matches_won = 0
        self.num_matches_drawn = 0
        self.num_matches_lost = 0
        self.policy = policy
        self.won = False

    def __str__(self):
        return self.name

    def place_initial_bet(self, minimum_bet: int, maximum_bet: int, count):
        return minimum_bet

    def force_amount_to_be_betted(self, amount: int):
        self.chips -= amount
        return amount

    def play_move(self, hand, dealer_up_card):  # This should be learnt - optimal solution is blackjack basic strategy
        if (hand.hand_strength < 4) or (hand.hand_strength < 12 and hand.has_soft_card_available()) or (
                dealer_up_card.value < 2):
            pass
        # Building the current state tuple
        current_state = (hand.hand_strength, hand.has_soft_card_available(), hand.can_split, dealer_up_card.value)

        # Getting the action to be performed for this current state
        # NOT CHECKING IF MOVE CAN BE DONE DUE TO CHIPS SINCE WE DON'T CARE ABOUT CHIPS
        action = self.policy.choose_next_action( current_state, hand.get_possible_moves(current_state))
        action = action.upper()


        # Recording the combination so that it may be rewarded
        self.policy.add_move_to_tree(current_state, action)
        chromosome = self.policy.chromosome

        # Returning the action
        return action, chromosome,current_state,hand.cards[-1]

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

    def getPlayerPerformance(self, writer, rounds, print_info):
        win_rate = 0
        ave_bank = 0
        ave_reward = 0
        actions2 = []
        for i in range(2):
            self.wins = 0
            self.games = 0
            self.bank = 1000.0

            for i in range(rounds):
                ave_reward2, actions = game(self, 4, False)
                ave_reward = ave_reward + ave_reward2
                actions2.append(actions)
                win_rate += (1.0 * (self.num_matches_won + (self.num_matches_drawn / 2))) / 5
        win_rate /= rounds
        ave_bank /= rounds
        ave_reward /= (rounds * 5)
        # print(actions2)
        if print_info == True: print(
            "Win rate: " + str(round(win_rate * 10.0, 1)) + " - Ave. reward: " + str(ave_reward))
        return win_rate, ave_bank, ave_reward, actions2

    def getPlayerPerformanceLearnt(self, rounds, print_info, strategy):
        win_rate = 0
        ave_bank = 0
        ave_reward = 0
        actions2 = []
        training = False
        for i in range(1):
            self.wins = 0
            self.games = 0
            self.bank = 1000.0
            for i in range(rounds):
                ave_reward2, actions, strategyReturned = game(self, 4, False)
                self.bank = self.chips
                ave_bank = ave_bank + self.bank
                ave_reward = ave_reward + ave_reward2
                actions2.append(actions)
                win_rate += (1.0 * (self.num_matches_won + (self.num_matches_drawn / 2))) / 5
                columns = []
                rows = []
                if win_rate * 10.0 >= MAX:
                    max=win_rate * 10.0
                softHand = False
                count = 0

                if strategy != None:
                    for x in range(len(strategyReturned)):
                        for y in range(len(strategyReturned[x])):
                            if strategyReturned[x][y]!='a' and ((win_rate * 10.0<=MAX-20) or (win_rate>MAX)):
                                strategyMain[x][y]=strategyReturned[x][y]

                    training = True


                self.won = False
                self.dealers_amount = []
                self.playersAmount = []
                self.softOrHard = []  # true = soft , false = hard
                self.splittable = []


        win_rate /= rounds
        ave_bank /= rounds
        ave_reward /= (rounds * 5)
        # print(actions2)
        if print_info == True: print(
            "Win rate: " + str(round(win_rate * 10.0, 1)) + " - Ave. reward: " + str(ave_reward))
        return win_rate, ave_bank, ave_reward, actions2,strategyMain , training


    def getPlayerStatus(self):
        if str(self) != 'Dealer':
            if self.hand.getScore() == 21:
                return 'BLACKJACK'
            elif self.hand.getScore() > 21:
                return 'BUST'
            else:
                return 'ALIVE'
        else:
            if self.hand.getScore() >= 17 and self.hand.getScore() < 21:
                return 'STOP_DEALER'
            elif self.hand.getScore() == 21:
                return 'BLACKJACK'
            elif self.hand.getScore() > 21:
                return 'BUST'
            else:
                return 'ALIVE'


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


class Chromosome():
    def __init__(self):
        super().__init__(0)
        self.hard = {}
        self.soft = {}
        self.special = {}
        self.splittable = {}

    def to_csv_string(self):
        lines = []
        for i in range(4, 22):
            line = []
            for j in range(2, 12):
                line.append(self.hard[(i, False, False, j)])
            lines.append(",".join(line))
        for i in range(12, 22):
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