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

from AI import AI
from Action import Action


class MyAI( AI ):

	class Board:
		def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
			self.remaining = totalMines
			self.rowDimension = rowDimension
			self.colDimension = colDimension
			self.board = [['*' for _ in range(rowDimension)] for _ in range(colDimension)]
			self.uncover(startX, startY, 0)  # starting tile guaranteed zero

		def uncover(self, x, y, label: int):
			self.board[x][y] = label

		def _isvalid(self, x, y):
			return (0 <= x < self.rowDimension) and (0 <= y < self.colDimension)

		def getLabel(self, x, y):
			return self.board[x][y]

		def getNumMarkedNeighbors(self, x, y):
			num = 0
			for col in range(x-1, x+2):
				for row in range(y-1, y+2):
					if col != x and row != y and self._isvalid(col, row) and self.getLabel(col, row) == "M":
						num += 1
			return num

		def getAdjacentCovered(self, x, y):
			num = 0
			for col in range(x-1, x+2):
				for row in range(y-1, y+2):
					if col != x and row != y and self._isvalid(col, row) and self.getLabel(col, row) == "*":
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


	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.board = MyAI.Board(rowDimension, colDimension, totalMines, startX, startY)
		self.board.printBoard()
	########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################


	def getAction(self, number: int) -> "Action Object":
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
