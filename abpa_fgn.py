from libFgn.chessPiece import ChessPiece
import random
import time

INF = 1000000
DEPTH = 6#是4的时候可以开启位置股价，6就不行
pieceTimePeriod = 0.5
moveTimePeriod = 0.5
f = open("out.txt", "w")

class Abpa:
	def __init__(self, down = True):
		self.down = down
		self.iWin = False
		self.initBoard()
		self.initPiece()
		self.lastOppStep = (2, 1)

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
		alpha = -INF
		beta = INF
		pieceStart = time.time()
		myPiecesSort = self.getSortPieces(self.lastOppStep[0], self.lastOppStep[1])
		for piece in myPiecesSort:
			#print(piece.name, "depth =", 1, "alpha =" , alpha, "beta =", beta, "start: {", file = f)
			pieceAlpha = -INF
			if not piece.alive:
				continue
			moveList = piece.getMoves()
			logX, logY = piece.x, piece.y
			moveStart = time.time()
			for move in moveList:
				die = piece.move(move[0], move[1])
				value = self.ab(1, -beta, -alpha, move)
				#revert
				piece.move(logX, logY)
				if die:
					die.alive = True
					self.board[die.x][die.y] = die
				#relax
				if value != INF+1:
					value = -value
					if value > pieceAlpha:
						pieceAlpha = value
					if value > alpha:
						alpha = value
						best = piece, move
					elif value == alpha and not self.board[best[1][0]][best[1][1]]:
						best = piece, move
				if time.time()-moveStart > moveTimePeriod:
					break
			#print(piece.name, "depth =", 1, "alpha =", alpha, "beta =", beta, "pieceAlpha = ", pieceAlpha, "}", file = f)
		#ori
		fromX, fromY, toX, toY = best[0].x, best[0].y, best[1][0], best[1][1]
		self.board[fromX][fromY].move(toX, toY)
		if not self.down:
			fromX, fromY, toX, toY = self.rotate(fromX, fromY, toX, toY)
		if not self.oppPieces[0].alive:
			self.iWin = True
		#print(alpha)
		return fromX, fromY, toX, toY

	def opponentMove(self, fromX, fromY, toX, toY):
		if not self.down:
			fromX, fromY, toX, toY = self.rotate(fromX, fromY, toX, toY)
		self.board[fromX][fromY].move(toX, toY)
		self.lastOppStep = (toX, toY)

	def getSortPieces(self, x, y):
		myPiecesSort = self.myPieces[:]
		random.shuffle(myPiecesSort)
		start = 0
		end = len(myPiecesSort)-1
		while start < end:
			if myPiecesSort[start].near(x, x):
				start += 1
			elif myPiecesSort[end].near(x, y):
				tmp = myPiecesSort[start]
				myPiecesSort[start] = myPiecesSort[end]
				myPiecesSort[end] = tmp
				start += 1
				end -= 1
			else:
				end -= 1
		return myPiecesSort

	def initBoard(self):
		self.board = [[None for i in range(9)] for i in range(10)]

	def initPiece(self):
		pieceType = [0, 1, 1, 2, 2, 6, 6, 6, 6, 6, 3, 3, 5, 5, 4, 4]
		myPiecePosition = [
			(0, 4),
			(0, 3), (0, 5),
			(0, 2), (0, 6),
			(3, 0), (3, 2), (3, 4), (3, 6), (3, 8),
			(0, 1), (0, 7),
			(2, 1), (2, 7),
			(0, 0), (0, 8)
		]
		oppPiecePosition = [
			(9, 4),
			(9, 3), (9, 5),
			(9, 2), (9, 6),
			(6, 0), (6, 2), (6, 4), (6, 6), (6, 8),
			(9, 1), (9, 7),
			(7, 1), (7, 7),
			(9, 0), (9, 8),
		]
		self.myPieces = [ChessPiece(pieceType[i], myPiecePosition[i], self.board, True) for i in range(len(pieceType))]
		self.oppPieces = [ChessPiece(pieceType[i], oppPiecePosition[i], self.board, False) for i in range(len(pieceType))]

	def rotate(self, fromX, fromY, toX, toY):
		fromX = 9 - fromX
		fromY = 8 - fromY
		toX = 9 - toX
		toY = 8 - toY
		return fromX, fromY, toX, toY

	def getValue(self, myPieces, oppPieces):
		'''if not myPieces[13].alive:
			print('***')
			self.check()'''
		value = 0
		for i in myPieces:
			if i.alive:
				#棋子价值评估
				value += i.value
				#棋子位置评估
				#value += i.getPositionValue()
		for i in oppPieces:
			if i.alive:
				#棋子价值评估
				value -= i.value
				#棋子位置评估
				#value -= i.getPositionValue()
		'''if not myPieces[13].alive:
			print(value)'''
		if value == -1000000:
			self.check()
		return value

	def ab(self, depth, alpha, beta, move):
		if depth&1 == 0:
			pieceList = self.myPieces
		else:
			pieceList = self.oppPieces
		if not pieceList[0].alive:
			return -INF+1
		if depth == DEPTH:
			if depth&1 == 0:
				return self.getValue(self.myPieces, self.oppPieces)
			else:
				return self.getValue(self.oppPieces, self.myPieces)
		myPiecesSort = self.getSortPieces(move[0], move[1])
		pieceStart = time.time()
		for piece in myPiecesSort:
			'''for i in range(depth):
				print("    ", end = '', file = f)
			print(piece.name, "depth =", depth, "alpha =" , alpha, "beta =", beta, "start: {", file = f)'''
			if not piece.alive:
				continue
			moveList = piece.getMoves()
			logX, logY = piece.x, piece.y
			moveStart = time.time()
			pieceAlpha = -INF
			for move in moveList:
				die = piece.move(move[0], move[1])
				value = self.ab(depth+1, -beta, -alpha, move)
				#revert
				piece.move(logX, logY)
				if die:
					die.alive = True
					self.board[die.x][die.y] = die
				#relax
				if value != INF+1:
					value = -value
					if value > pieceAlpha:
						pieceAlpha = value
					if value > alpha:
						alpha = value
					if value >= beta:
						'''for i in range(depth):
							print("    ", end = '', file = f)
						print(depth, "value = ", value, "return INF+1 }", file = f)'''
						return INF+1
				if time.time()-moveStart > moveTimePeriod**depth:
					break
			if time.time() - pieceStart > pieceTimePeriod**depth:
				break
			'''for i in range(depth):
				print("    ", end = '', file = f)
			print(piece.name, "depth =", depth, "alpha =", alpha, "beta =", beta, "pieceAlpha = ", pieceAlpha, "}", file = f)'''
		'''for i in range(depth):
			print("    ", end = '')
		print("depth =", depth, "alpha =", alpha)'''
		return alpha

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
