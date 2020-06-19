import csv
import math
import random
import random as rand
import numpy as np
from tree import *
from Player import *
strategyVar = [['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
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
# minimum bet
MIN_BET = 0.0
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
symbol_to_move_name = {
    'H': 'Hit',
    'S': 'Stand',
    'D': 'Double-down',
    'P': 'Split'
}
Hand_Object_list= []
Hand_values = []
Actions = []
states=[]
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


# this class is for a single Card
# a card object contains a rank (A,2,3,...), a suit (spades, clubs, etc.), and a score ('J' => 10, 'A' => 1, '2' => 2)
class Card:
    def __init__(self, suit, face, value):
        self.suit = suit
        self.face = face
        self.value = value

    def to_string(self):
        return '{ "suit": "' + str(self.suit) + '", "face": "' + str(self.face) + '", "value": "' + str(
            self.value) + '" }'

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


# this method returns an array of strings that are the types of a full deck of cards ('As', '2s', ..., 'Qd', 'Kd')
def getFullDeckArr():
    full_deck = [0] * 52
    for i in range(52):
        if i % 13 == 0:
            full_deck[i] = 'A'
        elif i % 13 == 9:
            full_deck[i] = 'T'
        elif i % 13 == 10:
            full_deck[i] = 'J'
        elif i % 13 == 11:
            full_deck[i] = 'Q'
        elif i % 13 == 12:
            full_deck[i] = 'K'
        else:
            full_deck[i] = str((i + 1) % 13)
    for i in range(13):
        full_deck[i] += 's'
    for i in range(13):
        full_deck[13 + i] += 'h'
    for i in range(13):
        full_deck[2 * 13 + i] += 'c'
    for i in range(13):
        full_deck[3 * 13 + i] += 'd'
    return full_deck


# this class is for a deck of cards
# a deck object contains an array of card objects
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

    # selects a random card in the deck object, deletes it, then returns it
    def deal(self):
        r = rand.randint(0, len(self.cards) - 1)
        self.drawn_cards.append(r)
        card = self.cards.pop(r)
        self.cards_drawn_since_last_shuffle += 1
        return card

    def draw_card(self):
        if (len(self.cards) == 1):
            print()
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
            j = random.randint(0, i + 1)
            # Swap arr[i] with the element at random index
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        self.cards_drawn_since_last_shuffle = 0


class Hand:
    def __init__(self, card1, card2, amount_betted):

        self.can_split = card1.face == card2.face
        self.has_doubled_down = False
        self.card1 = card1
        self.card2 = card2
        self.cards = [self.card1, self.card2]
        self.soft_cards_available = 0
        if self.card1.face == 'A' and self.card2.face == 'A':
            self.soft_cards_available += 2
        elif (self.card1.face == 'A' and self.card2.face != 'A') or (self.card2.face != 'A' and self.card2.face == 'A'):
            self.soft_cards_available += 1
        self.soft_cards_used = 0
        self.amount_betted_on_hand = amount_betted
        self.hand_strength = self.card1.value + self.card2.value
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
        self.amount_betted_on_hand += amount  # In case we have a double down

    def get_possible_moves(self,current_state):
        if (
                self.hand_strength > 21 and not current_state[1]) or self.hand_strength == 21 or self.has_doubled_down:
            return ['s']
        possible_moves = ['H', 's']
        if self.can_split:
            possible_moves.append('p')
        if len(self.cards) == 2:
            possible_moves.append('D')  # Double down only allowed when player has 2 cards in the hand
        return possible_moves

    def to_string(self):
        lines = ["hand: {"]
        for i in range(len(self.cards)):
            lines.append("card_" + str(i) + ": " + str(self.cards[i]))
        lines.append("}")
        return '\n'.join(lines)


# this method is a bit incomplete
# prints the end game results (e.g. 'dealer hit blackjack', 'player busts', etc.)
def printGameResults(player, dealer):
    if player.getPlayerStatus() == 'BLACKJACK':
        print(str(player) + " got blackjack! " + str(player) + " wins!")
    elif dealer.getPlayerStatus() == 'BLACKJACK':
        print("Dealer got blackjack. " + str(player) + " loses.")
    elif player.getPlayerStatus() == 'BUST':
        print(str(player) + " busted. " + str(player) + " loses.")

    elif dealer.getPlayerStatus() == 'BUST':
        print("Dealer busted! " + str(player) + " wins!")
    elif player.hand.getScore() > dealer.hand.getScore():
        print(str(player) + " got a higher score than the dealer! " + str(player) + " wins!")
    elif player.hand.getScore() < dealer.hand.getScore():
        print("Dealer got a higher score than " + str(player) + ". " + str(player) + " loses.")
    elif player.hand.getScore() == dealer.hand.getScore():
        print("Draw.")
    print(str(player) + " now has $" + str(player.bank))


# this method prints a UI for playing blackjack
# returns the reward of the player
class Blackjack:
    def __init__(self, players: list, minimum_bet: int = 1, maximum_bet: int = 1000, number_of_decks: int = 8,
                 shuffle_every: int = 20):
        self.dealer = Dealer()
        self.player = players[0]
        self.players = players
        self.minimum_bet = minimum_bet
        self.maximum_bet = maximum_bet

        self.player_hands = {self.player: ReplacementBinaryTree()}
        self.deck = Deck(number_of_decks)
        self.deck.shuffle_cards()
        self.deck.shuffle_cards()
        self.card_count = 0
        self.total_rounds_played = 0
        self.shuffle_every = shuffle_every

    def player_handsInput(self):

        self.player_hands[self.players[1]] = ReplacementBinaryTree(self.players[1].handClass)

    def draw_single_card(self):
        card = self.deck.draw_card()
        true_count_denominator = (((1 * 52) - self.deck.cards_drawn_since_last_shuffle - 1) / 52)
        if card.face in ['2', '3', '4', '5', '6']:
            self.card_count += 1 / true_count_denominator
        elif card.face in ['10', 'J', 'Q', 'K', 'A']:
            if true_count_denominator == 0:
                print()
            self.card_count -= 1 / (true_count_denominator + 5)
        return card

    def request_initial_bet_from_players(self):
        initial_bets = {}
        for player in self.players:
            initial_bets[player] = player.place_initial_bet(self.minimum_bet, self.maximum_bet, self.card_count)
        return initial_bets

    def draw_round_cards(self, initial_bets: dict):
        for player in self.players:
            card_1 = self.draw_single_card()
            card_2 = self.draw_single_card()
            player_hand = Hand(card_1, card_2, initial_bets[player])
            smt = self.player_hands
            self.player_hands[self.player].overwrite_root(player_hand)
        self.dealer.start_new_turn(self.draw_single_card(), self.draw_single_card())

    def request_actions_from_dealer(self):
        while self.dealer.play_turn() != 'S':
            self.dealer.add_new_card(self.draw_single_card())

    def request_actions_from_players(self):
        hand_strenght = None
        actions_list =[]
        for player in self.players:
            next_hands = self.player_hands[player].get_tree_as_list()
            player.dealers_amount.append(self.dealer.up_card.value)
            last_completed_hand = None
            # Keep on requesting the actions from the player for the given hand
            gameEnded = False
            while len(next_hands) != 0:
                target_hand = next_hands[0]
               # player.card_values.append(target_hand.cards[0])
               # player.card_values.append(target_hand.cards[1])
                Hand_values.append(target_hand.hand_strength)
                action,chromosome,state,hand_obj = player.play_move(target_hand, self.dealer.up_card)
                Actions.append(action)
                states.append(state)
                Hand_Object_list.append(hand_obj)

                actions_list.append(action)
                # If the player decides to stand
                if action == 'S' or action == 's':
                    action = 'S'

                    # Let the current hand be completed and get all of the remaining hands after this hand
                    last_completed_hand = target_hand
                    next_hands = self.player_hands[player].get_all_hands_after_hand(target_hand)

                    gameEnded = True
                # If the player decides to split
                elif action == 'P' or action == 'p':
                    action = 'P'
                  #  actions_list.append(action)
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
                    player.splittable.append(new_card_1.value)

                # If the player decides to double down
                elif action == 'D' or action == 'd':
                    action = 'D'
                  #  actions_list.append(action)
                    amount = player.force_amount_to_be_betted(target_hand.amount_betted_on_hand)
                    target_hand.add_amount_to_bet(amount)
                    target_hand.add_card(self.draw_single_card())
                    player.hand.has_doubled_down = True
                  #  player.card_values.append(target_hand.cards[-1])
                 #   last_completed_hand = target_hand
                  #  next_hands = self.player_hands[player].get_all_hands_after_hand(target_hand)

                    gameEnded = True

                else:
                    action = 'H'
                    #  actions_list.append(action)
                    target_hand.add_card(self.draw_single_card())
                   # player.card_values.append(target_hand.cards[-1])
                player.splittable.append(0)

                player.playersAmount.append(target_hand.hand_strength)
                if target_hand.soft_cards_available > 0:
                    player.softOrHard.append(True)
                else:
                    player.softOrHard.append(False)

                if target_hand.hand_strength >21:
                    gameEnded = True
            hand_strenght = next_hands


        return 0,actions_list, chromosome

    def request_actions_from_players_same_conditions(self):
        hand_strenght = None
        actions_list =[]
        extra_drawn_cards = []
        for player in self.players:
            extra_drawn_cards_cpy = extra_drawn_cards.copy()
            next_hands = self.player_hands[player].get_tree_as_list()
            last_completed_hand = None
            # Keep on requesting the actions from the player for the given hand
            gameEnded = False
            while len(next_hands) != 0:
                target_hand = next_hands[0]
               # player.card_values.append(target_hand.cards[0])
               # player.card_values.append(target_hand.cards[1])
                action,chromosome,state,hand_obj = player.play_move(target_hand, self.dealer.up_card)
                Actions.append(action)
                states.append(state)
                Hand_Object_list.append(hand_obj)
                Hand_values.append(target_hand.hand_strength)
                actions_list.append(action)
                # If the player decides to stand
                if action == 'S' or action == 's':
                    action = 'S'

                    # Let the current hand be completed and get all of the remaining hands after this hand
                    last_completed_hand = target_hand
                    next_hands = self.player_hands[player].get_all_hands_after_hand(target_hand)

                    gameEnded = True
                # If the player decides to split
                elif action == 'P' or action == 'p':
                    action = 'P'
                  #  actions_list.append(action)
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
                    player.splittable.append(new_card_1.value)

                # If the player decides to double down
                elif action == 'D' or action == 'd':
                    action = 'D'
                  #  actions_list.append(action)
                    amount = player.force_amount_to_be_betted(target_hand.amount_betted_on_hand)
                    target_hand.add_amount_to_bet(amount)
                    target_hand.add_card(self.draw_single_card())
                    player.hand.has_doubled_down = True
                  #  player.card_values.append(target_hand.cards[-1])
                 #   last_completed_hand = target_hand
                  #  next_hands = self.player_hands[player].get_all_hands_after_hand(target_hand)

                    gameEnded = True

                else:
                    action = 'H'
                    #  actions_list.append(action)
                    target_hand.add_card(self.draw_single_card())
                   # player.card_values.append(target_hand.cards[-1])
                player.splittable.append(0)

                player.playersAmount.append(target_hand.hand_strength)
                if target_hand.soft_cards_available > 0:
                    player.softOrHard.append(True)
                else:
                    player.softOrHard.append(False)

                if target_hand.hand_strength >21:
                    gameEnded = True
            hand_strenght = next_hands


        return 0,actions_list, chromosome



    def give_rewards(self):
        dealer_cards = [self.dealer.up_card, self.dealer.down_card]
        rewards = 0
        for card in self.dealer.hit_cards:
            dealer_cards.append(card)
        for player in self.players:
            player_hands = self.player_hands[player].get_tree_as_list()
            player_rewards = []
            for hand in player_hands:
                if hand.hand_strength > 21:

                    player_rewards.append(0)
                    #rewards = rewards+ 0
                elif hand.hand_strength < self.dealer.hand_strength:
                    player_rewards.append(0.1)
                    #rewards = rewards + ( (hand.hand_strength) / 21.0)
                elif hand.hand_strength == self.dealer.hand_strength:
                    player.won = True
                    self.player.wins = self.player.wins + 1
                    player_rewards.append(hand.amount_betted_on_hand)
                    #rewards = rewards + 1
                elif hand.hand_strength > self.dealer.hand_strength:
                    player.won = True
                    self.player.wins = self.player.wins + 1
                    player_rewards.append(hand.amount_betted_on_hand * 2)
                    #rewards = rewards + 1
            player.recieve_rewards([(player_hands[i], player_rewards[i]) for i in range(len(player_hands))],
                                   dealer_cards)

            self.player.wins = self.player.wins / len(player_hands)

        for x in range(len(player_rewards)):
            rewards = rewards + player_rewards[x]

        return rewards

    def play(self, number_of_rounds: int = 1, print_rounds_progress: bool = False):
        reward = 0
        next_milestone = 0
        for i in range(number_of_rounds):
            progress = (i / number_of_rounds) * 100
            self.total_rounds_played += 1
            if progress >= next_milestone:
                next_milestone += 10

            # Shuffle according to the total number of rounds played
            self.deck.shuffle_cards()
            self.card_count = 0
            # Requesting the initial bets from the players
            initial_bets = self.request_initial_bet_from_players()
            # Drawing the starting cards for the players and the dealer
            self.draw_round_cards(initial_bets)
            # Making the players play their turn until all of their hands have stood
            reward,actions,chromosome = self.request_actions_from_players()
            # Making the dealer do his moves
            self.request_actions_from_dealer()
            # Ending the round by giving the due rewards to the players (if they won or drew)
            reward = self.give_rewards()
            # Adding the cards of the deck back to the back of the deck
            self.deck.add_drawn_cards_back()

        return reward,actions,chromosome

    def play_same_conditions(self, number_of_rounds: int = 1, print_rounds_progress: bool = False):
        reward = 0
        next_milestone = 0
        for i in range(number_of_rounds):
            progress = (i / number_of_rounds) * 100
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
            extra_drawn_cards = []  # This will be used so that the players draw the same cards
            reward, actions, chromosome = self.request_actions_from_players_same_conditions()

            # Making the dealer take his actions
            self.request_actions_from_dealer()
            # Ending the round
            self.give_rewards()
            # Adding the cards of the deck back
            self.deck.add_drawn_cards_back()

        return reward,actions,chromosome


def game(player, deck_count, print_text):
    csv_row = []
    players = [player]

    blackjack = Blackjack(players, 1, 100, 8, 35)
    blackjack.player = player
    reward,actions,chromosome = blackjack.play(1, True)
    lines = chromosome.to_csv_string()
    handsObjs = Hand_Object_list
    acts = Actions
    sttt=states
    if player.won:
        for x in range(len(states)):

            if Hand_Object_list[x].value>=12:
                print()
            if not states[x][1] and not states[x][2]:
                if Hand_values[x]==4:
                    strategyVar[0][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==5:
                    strategyVar[1][states[x][3]-2]  = Actions[x]
                if Hand_values[x] == 6:
                    strategyVar[2][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==7:
                    strategyVar[3][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==8:
                    strategyVar[4][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==9:
                    strategyVar[5][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==10:
                    strategyVar[6][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==11:
                    strategyVar[7][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==12:
                    strategyVar[8][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==13:
                    strategyVar[9][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==14:
                    strategyVar[10][states[x][3]-2]  = Actions[x]
                if Hand_values[x] == 15:
                    strategyVar[11][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==16:
                    strategyVar[12][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==17:
                    strategyVar[13][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==18:
                    strategyVar[14][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==19:
                    strategyVar[15][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==20:
                    strategyVar[16][states[x][3]-2]  = Actions[x]
                if Hand_values[x]==21:
                    strategyVar[17][states[x][3]-2]  = Actions[x]


            elif states[x][1] and not states[x][2]:
                if Hand_Object_list[x].value==2:
                    strategyVar[18][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==3:
                    strategyVar[19][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value == 4:
                    strategyVar[20][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==5:
                    strategyVar[21][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==6:
                    strategyVar[22][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==7:
                    strategyVar[23][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==8:
                    strategyVar[24][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==9:
                    strategyVar[25][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==10:
                    strategyVar[26][states[x][3]-2]  = Actions[x]
            else:
                if Hand_Object_list[x].value==2:
                    strategyVar[27][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==3:
                    strategyVar[28][states[x][3]-2] = Actions[x]
                if Hand_Object_list[x].value == 4:
                    strategyVar[29][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==5:
                    strategyVar[30][states[x][3]-2] = Actions[x]
                if Hand_Object_list[x].value==6:
                    strategyVar[31][states[x][3]-2] = Actions[x]
                if Hand_Object_list[x].value==7:
                    strategyVar[32][states[x][3]-2] = Actions[x]
                if Hand_Object_list[x].value==8:
                    strategyVar[33][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==9:
                    strategyVar[34][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==10:
                    strategyVar[35][states[x][3]-2]  = Actions[x]
                if Hand_Object_list[x].value==11:
                    strategyVar[36][states[x][3]-2]  = Actions[x]
    states.clear()
    Hand_Object_list.clear()
    Actions.clear()
    Hand_values.clear()
    smt = strategyVar
    # with open('evol_neural_net2.csv', 'a') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(lines)
    learnt = []

    return reward,actions,strategyVar
