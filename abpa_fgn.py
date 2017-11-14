from libFgn.chessPiece import ChessPiece

class Abpa:
	def __init__(self, down = True):
		self.down = down
		self.initBoard()
		self.initPiece()
		self.check()
		#todo

	def myStep(self):
		#todo
		return fromX, fromY, toX, toY

	def opponentMove(self, fromX, fromY, toX, toY):
		# todo
		return fromX, fromY, toX, toY

	def check(self):
		for i in self.board:
			for j in i:
				if j:
					print(j.name, end = ' ')
				else:
					print('+', end = '  ')
			print()
		print()
		for i in range(9, -1, -1):
			print('|', end = '')
			for j in range(9):
				print(' (' + str(i) + ", " + str(j) + ") |", end = '')
			print()

	def initBoard(self):
		self.board = [[None for i in range(9)] for i in range(10)]

	def initPiece(self):
		pieceType = [4, 3, 2, 1, 0 ,1, 2, 3, 4, 5, 5, 6, 6, 6, 6, 6]
		redPiecePosition = [(0, i) for i in range(9)] +\
		                   [(2, 1), (2, 7)] +\
		                   [(3, i) for i in range(0, 9, 2)]
		blackPiecePosition = [(9, i) for i in range(9)] +\
		                     [(7, 1), (7, 7)] +\
		                     [(3, i) for i in range(0, 9, 2)]
		self.redPieces = [ChessPiece(pieceType[i], redPiecePosition[i]) for i in range(len(pieceType))]
		self.blackPiecces = [ChessPiece(pieceType[i], blackPiecePosition[i]) for i in range(len(pieceType))]
		for i in self.redPieces:
			self.board[i.x][i.y] = i
		for i in self.blackPiecces:
			self.board[i.x][i.y] = i


if __name__ == "__main__":
	play = Abpa()
