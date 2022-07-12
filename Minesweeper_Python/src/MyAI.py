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
from collections import namedtuple

from AI import AI
from Action import Action


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
					if self.isCovered(x, y):
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
					if self.getNumLabeledNeighbors(x, y) > 0:
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

		# basic outline of getAction()
		# TODO: are we done? Num of covered tiles == num of mines -> LEAVE
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

		# TODO: if EffectiveLabel(x) = 0, then all UnMarkedNeighbors(x) must be safe(you can UNCOVER them)
		return Action(AI.Action.LEAVE)
