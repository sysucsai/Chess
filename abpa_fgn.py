from libFgn.chessPiece import ChessPiece
import random

INF = 1000000

class Abpa:
	def __init__(self, down = True):
		self.down = down
		self.iWin = False
		self.initBoard()
		self.initPiece()

	def check(self, moveFrom = None, moveTo = None ,moveList = None):
		for i in range(len(self.board)-1, -1, -1):
			for j in range(len(self.board[i])):
				if moveList and (i, j) in moveList:
					print(':', end = '')
				elif moveFrom and moveFrom[0] == i and moveFrom[1] == j:
					print('{', end = '')
				elif moveTo and moveTo[0] == i and moveTo[1] == j:
					print('{', end = '')
				else:
					print(' ', end = '')
				if self.board[i][j]:
					print(self.board[i][j].name, end = '')
				else:
					print(' ＋ ', end = '')
				if moveList and (i, j) in moveList:
					print(':', end = '')
				elif moveFrom and moveFrom[0] == i and moveFrom[1] == j:
					print('}', end = '')
				elif moveTo and moveTo[0] == i and moveTo[1] == j:
					print('}', end = '')
				else:
					print(' ', end = '')
			print()
		print()

	def myStep(self):
		value, best = self.ab(0, -INF, +INF)
		fromX, fromY, toX, toY = best[0].x, best[0].y, best[1][0], best[1][1]
		self.board[fromX][fromY].move(toX, toY)
		if not self.down:
			fromX, fromY, toX, toY = self.rotate(fromX, fromY, toX, toY)
		if not self.oppPieces[4].alive:
			self.iWin = True
		return fromX, fromY, toX, toY

	def opponentMove(self, fromX, fromY, toX, toY):
		if not self.down:
			fromX, fromY, toX, toY = self.rotate(fromX, fromY, toX, toY)
		self.board[fromX][fromY].move(toX, toY)

	def initBoard(self):
		self.board = [[None for i in range(9)] for i in range(10)]

	def initPiece(self):
		pieceType = [4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 5, 6, 6, 6, 6, 6]
		myPiecePosition = [(0, i) for i in range(9)] +\
		                   [(2, 1), (2, 7)] +\
		                   [(3, i) for i in range(0, 9, 2)]
		oppPiecePosition = [(9, i) for i in range(9)] +\
		                     [(7, 1), (7, 7)] +\
		                     [(6, i) for i in range(0, 9, 2)]
		self.myPieces = [ChessPiece(pieceType[i], myPiecePosition[i], self.board, True) for i in range(len(pieceType))]
		self.oppPieces = [ChessPiece(pieceType[i], oppPiecePosition[i], self.board, False) for i in range(len(pieceType))]

	def rotate(self, fromX, fromY, toX, toY):
		fromX = 9 - fromX
		fromY = 8 - fromY
		toX = 9 - toX
		toY = 8 - toY
		return fromX, fromY, toX, toY

	def getValue(self, myPieces, oppPieces):
		value = 0
		myAlive = 0
		oppAlive = 0
		for i in myPieces:
			if i.alive:
				myAlive += 1
		for i in oppPieces:
			if i.alive:
				oppAlive += 1
		for i in myPieces:
			if i.alive:
				value += i.value
		for i in oppPieces:
			if i.alive:
				value += i.value
		return value

	def ab(self, depth, alpha, beta):
		if depth&1 == 0:
			pieceList = self.myPieces[:]
		else:
			pieceList = self.oppPieces[:]
		if not pieceList[4].alive:
			return -INF+1, None
		if depth == 4:
			if depth&1 == 0:
				return self.getValue(self.myPieces, self.oppPieces), None
			else:
				return self.getValue(self.oppPieces, self.myPieces), None
		best = None
		random.shuffle(pieceList)
		for piece in pieceList:
			if not piece.alive:
				continue
			moveList = piece.getMoves()
			random.shuffle(moveList)
			logX, logY = piece.x, piece.y
			for move in moveList:
				die = piece.move(move[0], move[1])
				value, trash = self.ab(depth+1, -beta, -alpha)
				value = -value
				if value > alpha:
					alpha = value
					best = (piece, move)
				#revert
				piece.move(logX, logY)
				if die:
					die.alive = True
					self.board[die.x][die.y] = die
				if value > beta:
					return beta, best
		return alpha, best

import sys
def compare(board1, board2):
	for i in range(10):
		for j in range(9):
			if board1[i][j]:
				if board2[9-i][8-j]:
					if board1[i][j].pieceType != board2[9-i][8-j].pieceType:
						print('ERROR :', board1[i][j].name, board2[9-i][8-j].name)
						sys.exit()
				else:
					print('ERROR :', i, j)
					print(board1[i][j], board2[9-i][8-j])
					sys.exit()
			if board2[9-i][8-j]:
				if board1[i][j]:
					if board1[i][j].pieceType != board2[9-i][8-j].pieceType:
						print('ERROR :', board1[i][j].name, board2[9-i][8-j].name)
						sys.exit()
				else:
					print('ERROR :', i, j)
					print(board1[i][j], board2[9-i][8-j])
					sys.exit()

if __name__ == "__main__":
	a = Abpa(False)
	b = Abpa(True)
	fromX, fromY, toX, toY = b.myStep()
	a.opponentMove(fromX, fromY, toX, toY)
	b.check((fromX, fromY), (toX, toY))
	compare(b.board, a.board)
	while (True):
		fromX, fromY, toX, toY = a.myStep()
		b.opponentMove(fromX, fromY, toX, toY)
		b.check((fromX, fromY), (toX, toY))
		compare(b.board, a.board)
		if a.iWin:
			print('[*] Win!')
			break
		fromX, fromY, toX, toY = b.myStep()
		a.opponentMove(fromX, fromY, toX, toY)
		b.check((fromX, fromY), (toX, toY))
		compare(b.board, a.board)
		if b.iWin:
			print('(*) Win!')
			break
