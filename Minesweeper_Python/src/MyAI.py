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
			# self.uncover(startX, startY, 0)  # starting tile guaranteed zero

		def uncover(self, x, y, label: int):
			self.board[x][y] = label

		def mark(self, x, y):
			self.uncover(x, y, "M")

		def _isvalid(self, x, y):
			return (0 <= x < self.colDimension) and (0 <= y < self.rowDimension)

		def getLabel(self, x, y):
			return self.board[x][y]

		def isMarked(self, x, y):
			return self.getLabel(x, y) == "M"

		def isCovered(self, x, y):
			return self.getLabel(x, y) == "*"

		def isLabeled(self, x, y):
			return isinstance(self.getLabel(x, y), int)

		def getCoveredCount(self):
			cnt = 0
			for x in range(self.colDimension):
				for y in range(self.rowDimension):
					if self.isCovered(x, y):
						cnt += 1
			return cnt

		def getMarkedNeighbors(self, x, y):
			neighbor = set()
			for col in range(x-1, x+2):
				for row in range(y-1, y+2):
					if not(col == x and row == y) and self._isvalid(col, row) and self.isMarked(col, row):
						neighbor.add((col, row))
			return neighbor

		def getNumMarkedNeighbors(self, x, y):
			return len(self.getMarkedNeighbors(x, y))

		def getNumLabeledNeighbors(self, x, y):
			num = 0
			for col in range(x-1, x+2):
				for row in range(y-1, y+2):
					if not(col == x and row == y) and self._isvalid(col, row) and isinstance(self.getLabel(col, row), int):
						num += 1
			return num

		def getCoveredNeighbors(self, x, y):
			neighbor = set()
			for col in range(x-1, x+2):
				for row in range(y-1, y+2):
					if (not(col == x and row == y)) and self._isvalid(col, row) and self.isCovered(col, row):
						neighbor.add((col, row))
			return neighbor

		def getNumCoveredNeighbors(self, x, y):
			return len(self.getCoveredNeighbors(x, y))


		def getAdjacentCovered(self, x, y):
			num = 0
			for col in range(x-1, x+2):
				for row in range(y-1, y+2):
					if not(col == x and row == y) and self._isvalid(col, row) and self.getLabel(col, row) == "*":
						num += 1
			return num

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
					adjacent = self.getAdjacentCovered(x, y)
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
		self.board = MyAI.Board(rowDimension, colDimension, totalMines, startX, startY)

		self.totalMines = totalMines
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

		# basic outline of getAction()
		# are we done? Num of covered tiles == num of mines -> LEAVE
		if self.board.getCoveredCount() == self.totalMines:
			return Action(AI.Action.LEAVE)

		# otherwise need to figure out UNCOVER X, Y
		# first get the frontier tiles
		covered_frontier = self.board.getCoveredFrontier()
		uncovered_fronter = self.board.getUncoveredFrontier()

		# use simple rule of thumb logic -> UNCOVER X, Y
		self.markAll(uncovered_fronter)
		action = self.ruleOfThumb(uncovered_fronter)
		if action is not None:
			self.lastActionPosition = (action.getX(), action.getY())
			if self.board.isMarked(action.getX(), action.getY()):
				raise
			print(action.getX(), action.getY())
			self.board.printBoard()
			return action

		# if this did not give tile to uncover, use better logic -> UNCOVER X, Y

		# if this did not give tile to uncover, go to even more sophisticated logic -> UNCOVER X, Y

		# finally, if still no tile (this will happen since some partial boards are undecidable), need to
		# guess - exact probability computation may be intractable, use approximation -> UNCOVER X, Y
		self.board.printBoard()
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def markAll(self, frontier):
		for x, y in frontier:
			covered_neighbor = self.board.getCoveredNeighbors(x, y)
			if self.board.getEffectiveLabel(x, y) == len(covered_neighbor):
				for x1, y1 in covered_neighbor:
					self.board.mark(x1, y1)

	def ruleOfThumb(self, frontier):
		# E.g. if EffectiveLabel(x) = NumUnMarkedNeighbors(x), then; all; UnMarkedNeighbors(x); must; be; mines(mark; them as such
		# on; the; board;this is likely; to; reduce; effective; labels; of; other; nearby; uncovered; tiles, so; that; the
		# rules; of; thumb; can; be; fired; again)
		for x, y in frontier:
			covered_neighbor = self.board.getCoveredNeighbors(x, y)
			marked_neighbor = self.board.getMarkedNeighbors(x, y)
			if covered_neighbor and (
					self.board.getLabel(x, y) == len(marked_neighbor) or self.board.getEffectiveLabel(x, y) == 0):
				# all mines neighboring this tile is marked, all neighbors are safe
				# or
				# E.g. if EffectiveLabel(x) = 0, then; all; UnMarkedNeighbors(x); must; be; safe(you; can; UNCOVER; them)
				next_x, next_y = covered_neighbor.pop()
				return Action(AI.Action.UNCOVER, next_x, next_y)
