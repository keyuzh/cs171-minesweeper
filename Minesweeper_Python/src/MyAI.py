# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
import math
from collections import namedtuple

from AI import AI
from Action import Action
from collections import defaultdict

class MyAI( AI ):

	class Board:
		def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
			self.remaining = totalMines
			self.rowDimension = rowDimension
			self.colDimension = colDimension
			self.board = [['*' for _ in range(rowDimension)] for _ in range(colDimension)]

		def uncover(self, x, y, label):
			self.board[x][y] = label

		def mark(self, x, y):
			self.uncover(x, y, "M")

		def isvalid(self, x, y):
			return (0 <= x < self.colDimension) and (0 <= y < self.rowDimension)

		def getLabel(self, x, y):
			return self.board[x][y]

		def isMarked(self, x, y):
			return self.getLabel(x, y) == "M"

		def isCovered(self, x, y):
			return self.getLabel(x, y) == "*"

		def isLabeled(self, x, y):
			return isinstance(self.getLabel(x, y), int)

		def distanceToEdge(self, x, y):
			max_x = self.colDimension - 1
			max_y = self.rowDimension - 1
			x_distance = min(x, max_x - x)
			y_distance = min(y, max_y - y)
			return x_distance + y_distance

		def distanceToPoint(self, p1: (int, int), p2: (int, int)):
			p1_x, p1_y = p1
			p2_x, p2_y = p2
			return math.sqrt((p1_x - p2_x)**2 + (p1_y - p2_y)**2)

		def getNumMarkedTiles(self):
			cnt = 0
			for x in range(self.colDimension):
				for y in range(self.rowDimension):
					if self.isMarked(x, y):
						cnt += 1
			return cnt

		def getAllCoveredTile(self):
			covered = set()
			for x in range(self.colDimension):
				for y in range(self.rowDimension):
					if self.isCovered(x, y):
						covered.add((x,y))
			return covered

		def getNeighbors(self, x, y):
			neighbor = set()
			for col in range(x-1, x+2):
				for row in range(y-1, y+2):
					if not(col == x and row == y) and self.isvalid(col, row):
						neighbor.add((col, row))
			return neighbor

		def getCoveredCount(self):
			"""Total number of covered tiles on the board."""
			cnt = 0
			for x in range(self.colDimension):
				for y in range(self.rowDimension):
					# if self.isCovered(x, y):
					if not self.isLabeled(x, y):
						cnt += 1
			return cnt

		def getMarkedNeighbors(self, x, y):
			return {(col, row) for col, row in self.getNeighbors(x, y) if self.isMarked(col, row)}

		def getNumMarkedNeighbors(self, x, y):
			return len(self.getMarkedNeighbors(x, y))

		def getLabeledNeighbors(self, x, y):
			return {(col, row) for col, row in self.getNeighbors(x, y) if self.isLabeled(col, row)}

		def getNumLabeledNeighbors(self, x, y):
			return len(self.getLabeledNeighbors(x, y))

		def getCoveredNeighbors(self, x, y):
			return {(col, row) for col, row in self.getNeighbors(x, y) if self.isCovered(col, row)}

		def getNumCoveredNeighbors(self, x, y):
			return len(self.getCoveredNeighbors(x, y))

		def getEffectiveLabel(self, x, y):
			# EffectiveLabel(x) = Label(x) - NumMarkedNeighbors(x)
			if isinstance(self.getLabel(x, y), int):
				return self.getLabel(x, y) - self.getNumMarkedNeighbors(x, y)

		def printBoard(self):
			print("  " + ''.join([6*" " + str(i) for i in range(self.rowDimension)]))
			for y in range(self.rowDimension):
				print(str(y) + " | ", end='')
				for x in range(self.colDimension):
					label = self.getLabel(x, y)
					effective = self.getEffectiveLabel(x, y)
					if effective is None:
						effective = ' '
					adjacent = self.getNumCoveredNeighbors(x, y)
					print("  {}:{}:{}".format(label, effective, adjacent), end='')
				print()

		def getUncoveredFrontier(self):
			frontier = set()
			for x in range(self.colDimension):
				for y in range(self.rowDimension):
					if self.isLabeled(x, y) and 0 < self.getNumCoveredNeighbors(x, y):
						frontier.add((x, y))
			return frontier

		def getCoveredFrontier(self):
			frontier = set()
			for x in range(self.colDimension):
				for y in range(self.rowDimension):
					if self.isCovered(x, y) and self.getNumLabeledNeighbors(x, y) > 0:
						frontier.add((x, y))
			return frontier

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		# initialize board
		self.board = MyAI.Board(rowDimension, colDimension, totalMines, startX, startY)
		# store total number of mines
		self.totalMines = totalMines
		# need a variable to store the position of the last uncovered tile
		self.lastActionPosition = (startX, startY)

		self.safe_tiles = set()

		self.broke = False
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def getAction(self, number: int) -> "Action Object":
		"""As you UNCOVER, FLAG, UNFLAG, update the board
		When you return UNCOVER, next getAction (number) call has the
		label of the square you uncovered"""
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		# update the label of last uncovered tile
		self.board.uncover(self.lastActionPosition[0], self.lastActionPosition[1], number)

		# debug
		self.board.printBoard()

		# TODO: edge case
		self.edgeCase()

		if self.safe_tiles:
			return self.return_action()

		# basic outline of getAction()
		# TODO: are we done? Num of covered tiles == num of mines -> LEAVE
		if self.board.getCoveredCount() == self.totalMines:
			return Action(AI.Action.LEAVE)
		# otherwise need to figure out UNCOVER X, Y

		# first get the frontier tiles
		covered_frontier = self.board.getCoveredFrontier()
		uncovered_frontier = self.board.getUncoveredFrontier()


		# TODO: use simple rule of thumb logic -> UNCOVER X, Y
		action = self.ruleOfThumb(uncovered_frontier)
		if action is not None:
			# rule of thumb returned an action, save the position of that action, then return
			self.lastActionPosition = (action.getX(), action.getY())
			return action

		# TODO: if this did not give tile to uncover, use better logic -> UNCOVER X, Y
		action = self.model_checking()
		if action is not None:
			# rule of thumb returned an action, save the position of that action, then return
			self.lastActionPosition = (action.getX(), action.getY())
			return action
		# TODO: if this did not give tile to uncover, go to even more sophisticated logic -> UNCOVER X, Y
		# TODO: finally, if still no tile (this will happen since some partial boards are undecidable), need to
		# guess - exact probability computation may be intractable, use approximation -> UNCOVER X, Y
		self.board.printBoard()
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def ruleOfThumb(self, frontier):
		# TODO: if EffectiveLabel(x) = NumCoveredNeighbors(x), then all UnMarkedNeighbors(x) must be mines(mark them as such
		# on the board. This is likely to reduce effective labels of other nearby uncovered tiles, so that the
		# rules of thumb can be fired again)
		for x in range(self.board.colDimension):
			for y in range(self.board.rowDimension):
				if self.board.getEffectiveLabel(x, y) == self.board.getNumCoveredNeighbors(x, y):
					neighbors = self.board.getCoveredNeighbors(x, y)
					for (x1, y1) in neighbors:
						self.board.mark(x1, y1)

		# TODO: if EffectiveLabel(x) = 0, then all UnMarkedNeighbors(x) must be safe(you can UNCOVER them)
		for x in range(self.board.colDimension):
			for y in range(self.board.rowDimension):
				if self.board.getEffectiveLabel(x, y) == 0:
					neighbors = self.board.getCoveredNeighbors(x, y)
					if not neighbors:
						continue
					self.safe_tiles = self.safe_tiles.union(neighbors)
					return self.return_action()

	def model_checking(self):
		self.board.printBoard()
		# divide and conquer
		# first we divide frontier into groups of connected frontier
		# if there is a disconnection in the middle, hopefully it will divide the frontier into groups smaller than 15,
		# otherwise divide manually
		frontiers = self.divide_step()
		i = 0
		while i < len(frontiers):
			if len(frontiers[i]) > 11:
				self.broke = True
				# if it is still too long after dividing, do it again
				half = len(frontiers[i]) // 2
				temp = frontiers[i]
				frontiers[i] = temp[:half]  # current index = first half
				frontiers.insert(i+1, temp[half:])  # insert second half after current index
				i += 1
			i += 1

		result = []
		for i in frontiers:
			res = self.divide_conquer(i)
			if res is not None:
				result.append(res)
		# conquer step
		# find the tile in "result" with smallest probability and assume it it safe
		smallest = min(result, key=(lambda x: x[1]))
		self.safe_tiles.add(smallest[0])
		return self.return_action()

	def divide_step(self):
		# list of list, inner list is sorted (x,y) tuples
		sorted_frontier_collection = list()
		covered_frontier = self.board.getCoveredFrontier()
		# if len(covered_frontier) < 13:
		# 	# if it is short dont divide
		# 	return [list(covered_frontier)]
		# while covered_frontier is not empty
		while covered_frontier:
			sorted_frontier = list()
			# find the tile that is closest to the edge of board
			closest = min(
				[(x, y, self.board.distanceToEdge(x, y)) for x, y in covered_frontier],
				# (x, y, distance)
				key=(lambda x: x[2]))
			closest_x_y = (closest[0], closest[1])
			# a queue of (x, y) to be added to sorted_frontier
			queue = [closest_x_y]
			while queue:
				first = queue.pop(0)
				# remove it from covered_frontier and add to sorted_frontier
				covered_frontier.remove(first)
				sorted_frontier.append(first)
				# add its neighbors and repeat
				neighbors = list(self.board.getCoveredNeighbors(first[0], first[1]).intersection(covered_frontier))
				if not neighbors:
					# if there is no neighbors do nothing
					continue
				# sort by distance and add the closest neighbor back to queue
				neighbors.sort(key=(lambda x: self.board.distanceToPoint(first, (x[0], x[1]))))
				queue.append(neighbors[0])
			sorted_frontier_collection.append(sorted_frontier)
		return sorted_frontier_collection



	def divide_conquer(self, covered_frontier):
		combinations = 2 ** len(covered_frontier)
		binary_length = len(covered_frontier)
		possible_assignments = list()
		print("N = ", binary_length)
		for i in range(combinations):
			covered_frontier_dict = dict()
			binary_i = bin(i)[2:]
			while len(binary_i) < binary_length:
				binary_i = '0' + binary_i
			for j in range(len(covered_frontier)):
				covered_frontier_dict[covered_frontier[j]] =  binary_i[j]
			if self.check_constraints(covered_frontier_dict) is True:
				possible_assignments.append(covered_frontier_dict)

		tile_count = defaultdict(int)
		for dictionary in possible_assignments:
			for k,v in dictionary.items():
				tile_count[k] += int(v)

		try:
			min_tile = min(tile_count.items(), key=lambda x: x[1])
			# change the value from raw count to probability
			min_tile = (min_tile[0], min_tile[1] / len(possible_assignments))
			return min_tile
		except ValueError as e:
			print(e)
			return None





	def check_constraints(self, covered: dict) -> bool:
		for x,y in self.board.getUncoveredFrontier():
			effective_label = self.board.getEffectiveLabel(x,y)
			neighbors = self.board.getCoveredNeighbors(x,y).intersection(covered.keys())
			if (not neighbors):
				continue
			if len(neighbors) < effective_label:
				effective_label = len(neighbors)
			sum = 0
			for x1, y1 in neighbors:
				sum += int(covered[x1,y1])
			if sum != effective_label:
				return False
		return True






	def return_action(self):
		x, y = self.safe_tiles.pop()
		action = Action(AI.Action.UNCOVER, x, y)
		self.lastActionPosition = (action.getX(), action.getY())
		print(x, y)
		assert self.board.isCovered(x, y)
		return action

	def edgeCase(self):
		if self.totalMines == self.board.getNumMarkedTiles():
			# Uncover everything
			self.safe_tiles.union(self.board.getAllCoveredTile())
