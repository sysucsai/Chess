import timeit

class Board:
    def __init__(self):
        #棋盘范围
        self.rank_top = 3
        self.rank_bottom = 12
        self.file_left = 3
        self.file_right = 11

        #棋子编号
        self.piece_king = 0
        self.piece_advisor = 1
        self.piece_bishop = 2
        self.piece_knight = 3
        self.piece_rook = 4
        self.piece_cannon = 5
        self.piece_pawn = 6

        #其他常数
        self.max_gen_moves = 128  #最大生成走法数
        self.limit_depth = 32  #最大搜索深度
        self.mate_value = 10000     #最大分值，将死分值
        self.win_value = mate_value - 100       #胜棋分值
        self.advanced_value = 3     #先行权分值

        #判断是否在棋盘中
        self.ccInBoard = (
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        )

        #判断是否在九宫格中
        self.ccInFort = (
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        )

        #判断符合特定走法规则，1=将，2=士，3=帅
        self.ccLegalSpan = (
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0
        )

        #判断马的绊脚
        self.ccKnightPin = (
            0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,-16,  0,-16,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0, -1,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0, -1,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0, 16,  0, 16,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0
        )

        self.ccKingDelta = (-16, -1, 1, 16)  #帅的步长
        self.ccAdvisorDelta = (-17, -15, 15, 17)  #士的步长
        self.ccKnightDelta = ((-33, -31),(-18, 14),(-14, 18),(31, 33))  #马的步长，以帅的步长为马腿
        self.ccKnightCheckDelta = ((-33, -18),(-31, -14),(14, 31),(18, 33))  #马的步长，以士的步长为马腿

        #棋盘的初始设置
        self.cucpcStartup = (
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0, 20, 19, 18, 17, 16, 17, 18, 19, 20,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0, 21,  0,  0,  0,  0,  0, 21,  0,  0,  0,  0,  0,
            0,  0,  0, 22,  0, 22,  0, 22,  0, 22,  0, 22,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0, 14,  0, 14,  0, 14,  0, 14,  0, 14,  0,  0,  0,  0,
            0,  0,  0,  0, 13,  0,  0,  0,  0,  0, 13,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0, 12, 11, 10,  9,  8,  9, 10, 11, 12,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
        )

        #棋子位置棋力表
        self.cucvlPiecePos = (
            #king
            (
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  2,  2,  2,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0, 11, 15, 11,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
            )
            #advisor
            (
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0, 20,  0, 20,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0, 23,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0, 20,  0, 20,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
            )
            #bishop
            (
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0, 20,  0,  0,  0, 20,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0, 18,  0,  0,  0, 23,  0,  0,  0, 18,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0, 20,  0,  0,  0, 20,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
            )
            #knight
            (
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0, 90, 90, 90, 96, 90, 96, 90, 90, 90,  0,  0,  0,  0,
                0,  0,  0, 90, 96,103, 97, 94, 97,103, 96, 90,  0,  0,  0,  0,
                0,  0,  0, 92, 98, 99,103, 99,103, 99, 98, 92,  0,  0,  0,  0,
                0,  0,  0, 93,108,100,107,100,107,100,108, 93,  0,  0,  0,  0,
                0,  0,  0, 90,100, 99,103,104,103, 99,100, 90,  0,  0,  0,  0,
                0,  0,  0, 90, 98,101,102,103,102,101, 98, 90,  0,  0,  0,  0,
                0,  0,  0, 92, 94, 98, 95, 98, 95, 98, 94, 92,  0,  0,  0,  0,
                0,  0,  0, 93, 92, 94, 95, 92, 95, 94, 92, 93,  0,  0,  0,  0,
                0,  0,  0, 85, 90, 92, 93, 78, 93, 92, 90, 85,  0,  0,  0,  0,
                0,  0,  0, 88, 85, 90, 88, 90, 88, 90, 85, 88,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
            )
            #rook
            (
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,206,208,207,213,214,213,207,208,206,  0,  0,  0,  0,
                0,  0,  0,206,212,209,216,233,216,209,212,206,  0,  0,  0,  0,
                0,  0,  0,206,208,207,214,216,214,207,208,206,  0,  0,  0,  0,
                0,  0,  0,206,213,213,216,216,216,213,213,206,  0,  0,  0,  0,
                0,  0,  0,208,211,211,214,215,214,211,211,208,  0,  0,  0,  0,
                0,  0,  0,208,212,212,214,215,214,212,212,208,  0,  0,  0,  0,
                0,  0,  0,204,209,204,212,214,212,204,209,204,  0,  0,  0,  0,
                0,  0,  0,198,208,204,212,212,212,204,208,198,  0,  0,  0,  0,
                0,  0,  0,200,208,206,212,200,212,206,208,200,  0,  0,  0,  0,
                0,  0,  0,194,206,204,212,200,212,204,206,194,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
            )
            #cannon
            (
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,100,100, 96, 91, 90, 91, 96,100,100,  0,  0,  0,  0,
                0,  0,  0, 98, 98, 96, 92, 89, 92, 96, 98, 98,  0,  0,  0,  0,
                0,  0,  0, 97, 97, 96, 91, 92, 91, 96, 97, 97,  0,  0,  0,  0,
                0,  0,  0, 96, 99, 99, 98,100, 98, 99, 99, 96,  0,  0,  0,  0,
                0,  0,  0, 96, 96, 96, 96,100, 96, 96, 96, 96,  0,  0,  0,  0,
                0,  0,  0, 95, 96, 99, 96,100, 96, 99, 96, 95,  0,  0,  0,  0,
                0,  0,  0, 96, 96, 96, 96, 96, 96, 96, 96, 96,  0,  0,  0,  0,
                0,  0,  0, 97, 96,100, 99,101, 99,100, 96, 97,  0,  0,  0,  0,
                0,  0,  0, 96, 97, 98, 98, 98, 98, 98, 97, 96,  0,  0,  0,  0,
                0,  0,  0, 96, 96, 97, 99, 99, 99, 97, 96, 96,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
            )
            #pawn
            (
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  9,  9,  9, 11, 13, 11,  9,  9,  9,  0,  0,  0,  0,
                0,  0,  0, 19, 24, 34, 42, 44, 42, 34, 24, 19,  0,  0,  0,  0,
                0,  0,  0, 19, 24, 32, 37, 37, 37, 32, 24, 19,  0,  0,  0,  0,
                0,  0,  0, 19, 23, 27, 29, 30, 29, 27, 23, 19,  0,  0,  0,  0,
                0,  0,  0, 14, 18, 20, 27, 29, 27, 20, 18, 14,  0,  0,  0,  0,
                0,  0,  0,  7,  0, 13,  0, 16,  0, 13,  0,  7,  0,  0,  0,  0,
                0,  0,  0,  7,  0,  7,  0, 15,  0,  7,  0,  7,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
            )
        )

    #是否在棋盘中
    def in_board(sq):
        return (self.ccInBoard[sq] != 0)

    #是否在九宫格中
    def in_fort(sq):
        return (self.ccInFort[sq] != 0)

    #获得格子的横坐标
    def rank_y(sq):
        return (sq >> 4)

    #获得格子的纵坐标
    def file_x(sq):
        return (sq & 15)

    #根据横纵坐标获得格子
    def coord_xy(x, y):
        return (x + (y << 4))

    #反转格子
    def square_flip(sq):
        return (254 - sq)

    #纵坐标水平镜像
    def file_flip(x):
        return (14 - x)

    #横坐标垂直镜像
    def rank_flip(y):
        return (15 - y)

    #格子水平镜像
    def mirror_square(sq):
        return self.coord_xy(self.file_flip(self.file_x(sq)), self.rank_y(sq))

    #格子水平镜像
    def square_forward(sq, sd):
        return (sq - 16 + (sd << 5))

    #走法是否符合将的步长
    def king_span(sqSrc, sqDst):
        return (self.ccLegalSpan[sqDst - sqSrc + 256] == 1)

    #走法是否符合士的步长
    def advisor_span(sqSrc, sqDst):
        return (self.ccLegalSpan[sqDst - sqSrc + 256] == 2)

    #走法是否符合象的步长
    def bishop_span(sqSrc, sqDst):
        return (self.ccLegalSpan[sqDst - sqSrc + 256] == 3)

    #象腿的位置
    def bishop_pin(sqSrc, sqDst):
        return ((sqSrc + sqDst) >> 1)

    #马腿的位置
    def knight_pin(sqSrc, sqDst):
        return (sqSrc + self.ccKnightPin[sqDst - sqSrc + 256])

    #是否未过河
    def home_half(sq, sd):
        return ((sq & 0x80) != (sd << 7))

    #是否已过河
    def away_half(sq, sd):
        return ((sq & 0x80) == (sd << 7))

    #是否在河的同一边
    def same_half(sqSrc, sqDst):
        return (((sqSrc ^ sqDst) & 0x80) == 0)

    #是否在同一行
    def same_rank(sqSrc, sqDst):
        return (((sqSrc ^ sqDst) & 0xf0) == 0)

    #是否在同一列
    def same_file(sqSrc, sqDst):
        return (((sqSrc ^ sqDst) & 0x0f) == 0)

    #获得红黑标记，红子是8，黑子是16
    def side_tag(sd):
        return (8 + (sd << 3))

    #获得对方红黑标记
    def opp_side_tag(sd):
        return (16 - (sd << 3))

    #获得走法的起点
    def src(mv):
        return (mv & 255)

    #获得走法的终点
    def dst(mv):
        return (mv >> 8)

    #根据起点和终点获得走法
    def move(sqSrc, sqDst):
        return (sqSrc + sqDst * 256)

    #走法水平镜像
    def mirror_move(mv):
        return self.move(self.mirror_square(self.src(mv)), self.mirror_square(self.dst(mv)))




class Position:
    def __init__(self):
        #Board = Board
        self.sdPlayer = 0   #轮到谁走，0=红，1=黑
        self.ucpcSquares = []      #棋盘上的棋子
        for i in range(256):
            self.ucpcSquares.append(0)
        self.vlWhite = 0      #红子棋力
        self.vlBlack = 0       #黑子棋力
        self.nDistance = 0      #距离根节点的步数
        self.StartUp()

    #添加棋子
    def AddPiece(sq, pc):
        self.ucpcSquares[sq] = pc
        if pc < 16:
            self.vlWhite += Board.cucvlPiecePos[pc - 8][sq]
        else :
            self.vlBlack += Board.cucvlPiecePos[pc - 16][Board.square_flip(sq)]
    
    #删除棋子
    def DelPiece(sq, pc):
        self.ucpcSquares[sq] = 0
        if pc < 16:
            self.vlWhite -= Board.cucvlPiecePos[pc - 8][sq]
        else :
            self.vlBlack -= Board.cucvlPiecePos[pc - 16][Board.square_flip(sq)]

    #初始化棋盘
    def StartUp():
        for i in range(256):
            pc = Board.cucpcStartup[sq]
            if pc != 0:
                self.AddPiece(sq, pc)

    #交换走步方
    def ChangeSide():
        self.sdPlayer = 1 - sdPlayer

    #局面估值函数
    def Evaluate():
        if self.sdPlayer == 0:
            return (self.vlWhite - self.vlBlack)
        else :
            return (self.vlBlack - self.vlWhite)

    #搬一步棋的棋子
    def MovePiece(mv):
        sqSrc = self.src(mv)
        sqDst = self.dst(mv)
        pcCaptured = self.ucpcSquares[sqDst]
        if pcCaptured != 0:
            self.DelPiece(sqDst, pcCaptured)
        pc = self.ucpcSquares[sqSrc]
        self.DelPiece(sqSrc, pc)
        self.AddPiece(sqDst, pc)
        return self.pcCaptured

    #撤销搬一步棋的棋子
    def UndoMovePiece(mv, pcCaptured):
        sqSrc = self.src(mv)
        sqDst = self.dst(mv)
        pc = self.ucpcSquares[self.sqDst]
        self.DelPiece(sqDst, pc)
        self.AddPiece(sqSrc, pc)
        if pcCaptured != 0:
            self.AddPiece(sqDst, pcCaptured)

    #走一步棋,因为不能传引用，每次调用都应该加上一句第二个参数=MovePiece(mv)
    def MakeMove(mv):
        pcCaptured = self.MovePiece(mv)
        if self.Checked():
            self.UndoMovePiece(mv, pcCaptured)
            return False
        ChangeSide()
        self.nDistance += 1
        return True

    #生成所有走法
    def GenerateMoves(mvs):
        nGenMoves = 0
        pcSelfSide = self.side_tag(self.sdPlayer)
        pcOppSide = self.opp_side_tag(self.sdPlayer)
        for sqSrc in range(256):
            pcSrc = self.ucpcSquares[sqSrc]
            if (pcSrc & pcSelfSide) == 0:
                continue
            if pcSrc - pcSelfSide == Board.piece_king:
                for i in range(4):
                    sqDst = sqSrc + Board.ccKingDelta[i]
                    if Board.in_fort(sqDst) != True:
                        continue
                    pcDst = self.ucpcSquares[sqDst]
                    if (pcDst & pcSelfSide) == 0:
                        mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                        nGenMoves += 1
            if pcSrc - pcSelfSide == Board.piece_advisor:
                for i in range(4):
                    sqDst = sqSrc + Board.ccAdvisorDelta[i]
                    if Board.in_fort(sqDst) != True:
                        continue
                    pcDst = self.ucpcSquares[sqDst]
                    if (pcDst & pcSelfSide) == 0:
                        mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                        nGenMoves += 1
            if pcSrc - pcSelfSide == Board.piece_bishop:
                for i in range(4):
                    sqDst = sqSrc + Board.ccAdvisorDelta[i]
                    if Board.in_board(sqDst) != True and Board.home_half(sqDst, sdPlayer) and self.ucpcSquares[sqDst] == 0:
                        continue
                    sqDst += Board.ccAdvisorDelta[i]
                    pcDst = self.ucpcSquares[sqDst]
                    if (pcDst & pcSelfSide) == 0:
                        mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                        nGenMoves += 1
            if pcSrc - pcSelfSide == Board.piece_knight:
                for i in range(4):
                    sqDst = sqSrc + Board.ccKingDelta[i]
                    if self.ucpcSquares[sqDst] != 0:
                        continue
                    for j in range(2):
                        sqDst = sqSrc + Board.ccKnightDelta[i][j]
                        if Board.in_board(sqDst) != True:
                            continue
                        pcDst = self.ucpcSquares[sqDst]
                        if (pcDst & pcSelfSide) == 0:
                            mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                            nGenMoves += 1
            if pcSrc - pcSelfSide == Board.piece_rook:
                for i in range(4):
                    nDelta = Board.ccKingDelta[i]
                    sqDst = sqSrc + nDelta
                    while Board.in_board(sqDst):
                        pcDst = self.ucpcSquares[sqDst]
                        if pcDst == 0:
                            mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                            nGenMoves += 1
                        else :
                            if (pcDst & pcOppSide) != 0:
                                mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                                nGenMoves += 1
                            break
                        sqDst += nDelta
            if pcSrc - pcSelfSide == Board.piece_cannon:
                for i in range(4):
                    nDelta = Board.ccKingDelta[i]
                    sqDst = sqSrc + nDelta
                    while Board.in_board(sqDst):
                        pcDst = self.ucpcSquares[sqDst]
                        if pcDst == 0:
                            mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                            nGenMoves += 1
                        else :
                            break
                        sqDst += nDelta
                    sqDst += nDelta
                    while Board.in_board(sqDst):
                        pcDst = self.ucpcSquares[sqDst]
                        if pcDst != 0:
                            if (pcDst & pcOppSide) != 0:
                                mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                                nGenMoves += 1
                            break
                        sqDst += nDelta
            if pcSrc - pcSelfSide == Board.piece_pawn:
                sqDst = Board.square_forward(sqSrc, self.sdPlayer)
                if Board.in_board(sqDst):
                    pcDst = self.ucpcSquares[sqDst]
                    if (pcDst & pcSelfSide) == 0:
                        mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                        nGenMoves += 1
                if Board.away_half(sqSrc, self.sdPlayer):
                    for nDelta in range(-1, 2, 2):
                        sqDst = sqSrc + nDelta
                        if Board.in_board(sqDst):
                            pcDst = self.ucpcSquares[sqDst]
                            if (pcDst & pcSelfSide) == 0:
                                mvs[nGenMoves] = Board.move(sqSrc, sqDst)
                                nGenMoves += 1
        return nGenMoves

    #判断走步是否合法
    def LegalMove(mv):
        sqSrc = Board.src(mv)
        pcSrc = self.ucpcSquares[sqSrc]
        pcSelfSide = self.side_tag(self.sdPlayer)
        if (pcSrc & pcSelfSide) == 0:
            return False

        sqDst = Board.dst(mv)
        pcDst = self.ucpcSquares[sqDst]
        if (pcDst & pcSelfSide) != 0:
            return False

        if pcSrc - pcSelfSide == Board.piece_king:
            return (Board.in_fort(sqDst) and Board.king_span(sqSrc, sqDst))
        if pcSrc - pcSelfSide == Board.piece_advisor:
            return (Board.in_fort(sqDst) and Board.advisor_span(sqSrc, sqDst))
        if pcSrc - pcSelfSide == Board.piece_bishop:
            return (Board.same_half(sqSrc, sqDst) and Board.bishop_span(sqSrc, sqDst) and self.ucpcSquares[Board.bishop_pin(sqSrc, sqDst)] == 0)
        if pcSrc - pcSelfSide == Board.piece_knight:
            sqPin = Board.knight_pin(sqSrc, sqDst)
            return sqPin != (sqSrc and self.ucpcSquares[sqPin] == 0)
        if pcSrc - pcSelfSide == Board.piece_rook or pcSrc - pcSelfSide == Board.piece_cannon:
            if Board.same_rank(sqSrc, sqDst):
                if sqDst < sqSrc:
                    nDelta = -1
                else :
                    nDelta = 1
            elif Board.same_file(sqSrc, sqDst):
                if sqDst < sqSrc:
                    nDelta = -16
                else :
                    nDelta = 16
            else :
                return False
            sqPin = sqSrc + nDelta
            while (sqPin != sqDst) and (self.ucpcSquares[sqPin] == 0) :
                sqPin += nDelta
            if sqPin == sqDst:
                return (pcDst == 0) or (pcSrc - pcSelfSide == Board.piece_rook)
            elif (pcDst != 0) and (pcSrc - pcSelfSide == Board.piece_cannon):
                sqPin += nDelta
                while (sqPin != sqDst) and (self.ucpcSquares[sqPin] == 0):
                    sqPin += nDelta
                return (sqPin == sqDst)
            else :
                return False
        if pcSrc - pcSelfSide == Board.piece_pawn:
            if Board.away_half(sqDst, self.sdPlayer) and ((sqDst == sqSrc - 1) or (sqDst == sqSrc + 1)):
                return True
            return sqDst == Board.square_forward(sqSrc, self.sdPlayer)
        else :
            return False

    #判断是否被将军
    def Checked():
        sqSrc = 0
        pcSelfSide = self.side_tag(self.sdPlayer)
        pcOppSide = self.opp_side_tag(self.sdPlayer)

        for sqSrc in range(256):
            #找到将
            if self.ucpcSquares[sqSrc] != pcSelfSide + Board.piece_king:
                continue
            #将是否被兵将军
            if self.ucpcSquares[Board.square_forward(sqSrc, self.sdPlayer)] == (pcOppSide + Board.piece_pawn):
                return True
            for nDelta in (-1, 2, 2):
                if self.ucpcSquares[sqSrc + nDelta] == pcOppSide + Board.piece_pawn:
                    return True

            #是否被马将军
            for i in range (4):
                if self.ucpcSquares[sqSrc + Board.ccAdvisorDelta[i]] != 0:
                    continue
                for j in range(2):
                    pcDst = self.ucpcSquares[sqSrc + Board.ccKnightCheckDelta[i][j]]
                    if pcDst == pcOppSide + Board.piece_knight:
                        return True

            #判断是否被车or炮将军or被对方将骑脸
            for i in range(4):
                nDelta = Board.ccKingDelta[i]
                sqDst = sqSrc + nDelta
                while Board.in_board(sqDst):
                    pcDst = self.ucpcSquares[sqDst]
                    if pcDst != 0:
                        if pcDst == pcOppSide + Board.piece_rook or pcDst == pcOppSide + Board.piece_king:
                            return True
                        break
                    sqDst += nDelta
                sqDst += nDelta
                while Board.in_board(sqDst):
                    pcDst = self.ucpcSquares[sqDst]
                    if pcDst != 0:
                        if pcDst == pcOppSide + Board.piece_cannon:
                            return True
                        break
                    sqDst += nDelta
            return False
        return False

    #判断是否被杀
    def IsMate():
        mvs = []
        for ct in Board.max_gen_moves:
            mvs.append(0)
        nGenMoves = self.GenerateMoves(mvs)
        for i in nGenMoves:
            pcCaptured = self.MovePiece(mvs[i])
            if self.Checked() != True:
                self.UndoMovePiece(mvs[i], pcCaptured)
                return False
            else:
                self.UndoMovePiece(mvs[i], pcCaptured)
        return True

class Abpa:
    def __init__(self, down = True):
        self.pos = wlModule.Position()
        self.mvResult = 0
        self.nHistoryTable = []            

    def CompareHistory(lpmv1, lpmv2):
        return (self.nHistoryTable[lpmv1] - self.nHistoryTable[lpmv2])

    def SearchFull(vlAlpha, vlBeta, nDepth):
        mvs = []
        for i in self.chb.max_gen_moves:
            mvs.append(0)

        if nDepth == 0:
            return self.pos.Evalute()

        vlBest = -Board.mate_value
        mvBest = 0

        nGenMoves = self.pos.GenerateMoves(mvs)
        sorted(mvs, cmp=lambda x,y:self.CompareHistory(x, y))

        for i in nGenMoves: 
            pcCaptured = self.pos.MovePiece(mvs[i])
            if pos.MakeMove(mvs[i], pcCaptured):
                vl = -self.SearchFull(-vlBeta, -vlAlpha, nDepth-1)
                self.pos.UndoMovePiece(mvs[i], pcCaptured)

                if vl > vlBest:
                    vlBest = vl
                    if vl >= vlBeta:
                        mvBest = mvs[i]
                        break
                    if vl > vlAlpha:
                        mvBest = mvs[i]
                        vlAlpha = vl
        if vlBest == -Board.mate_value :
            return (self.pos.nDistance - Board.mate_value)
        if mvBest != 0:
            self.nHistoryTable[mvBest] += nDepth * nDepth
            if self.pos.nDistance == 0:
                self.mvResult = mvBest
        return vlBest

    def SearchMain():
        for i in range(65536):
            self.nHistoryTable.append(0)
        #t = timeit.Timer()
        self.pos.nDistance = 0

        for i in Board.limit_depth:
            vl = self.SearchFull(-Board.mate_value, Board.mate_value, i+1)
            if vl > Board.win_value or vl < Board.win_value:
                break
            #if timer - t > 1 sec break





