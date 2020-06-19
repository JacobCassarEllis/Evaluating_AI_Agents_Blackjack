import sys, os

'''
This class contains the data structure used to hold all of the player's hands.
Whenever the player splits his hand a new ReplacementBinaryTreeNode is created.
'''

class ReplacementBinaryTreeNode:
	def __init__(self, hand):
		self.hand = hand # This will be None whenever this node has children
		self.left = None
		self.right = None

	def replace(self, hand_to_be_replaced, replacement_1, replacement_2):
		if self.hand != None:
			if self.hand == hand_to_be_replaced:
				self.hand = None
				self.left = ReplacementBinaryTreeNode(replacement_1)
				self.right = ReplacementBinaryTreeNode(replacement_2)
				return True
			else:
				return False
		else:
			was_replaced = self.left.replace(hand_to_be_replaced, replacement_1, replacement_2)
			if was_replaced: return True
			was_replaced = self.right.replace(hand_to_be_replaced, replacement_1, replacement_2)
			if was_replaced: return True
		return False

	def get_sub_tree_as_list(self, output_list: list):
		if self.hand != None:
			output_list.append(self.hand)
		else:
			self.left.get_sub_tree_as_list(output_list)
			self.right.get_sub_tree_as_list(output_list)

	def get_all_hands_after_hand(self, hand, was_found: bool, output_list: list):
		if self.hand != None:
			if was_found:
				output_list.append(self.hand)
				return was_found
			elif self.hand == hand:
				was_found = True
				return was_found
			else:
				return was_found
		else:
			was_found = self.left.get_all_hands_after_hand(hand, was_found, output_list)
			was_found = self.right.get_all_hands_after_hand(hand, was_found, output_list)
			return was_found

class ReplacementBinaryTree:
	def __init__(self, initial_hand = None):
		if initial_hand != None:
			self.root = ReplacementBinaryTreeNode(initial_hand)
		else:
			self.root = None

	def is_empty(self):
		return self.root == None

	def overwrite_root(self, hand):
		self.root = ReplacementBinaryTreeNode(hand)

	def replace(self, hand, replacement_1, replacement_2):
		was_replaced = self.root.replace(hand, replacement_1, replacement_2)
		return was_replaced

	def get_tree_as_list(self): # Postorder traversal
		output_list = []
		self.root.get_sub_tree_as_list(output_list)
		return output_list

	def get_all_hands_after_hand(self, hand):
		output_list = []
		self.root.get_all_hands_after_hand(hand, False, output_list)
		return output_list
