# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from cchess2 import *
from threading import Lock, Thread

import abpa_fgn

lock2 = Lock()

class myThread(Thread):
    def __init__(self,side,fun):
        super(myThread, self).__init__()
        self.side = side
        self.fun = fun
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.fun(self.side)

    def quit(self):
        self.running = False

class piece(QLabel):
    def __init__(self,side, id, x, y, parent):
        super(piece, self).__init__(parent)
        self.parent = parent
        self.side = side
        self.id = id
        self.x = x
        self.y = y

    def mousePressEvent(self, QMouseEvent):
        self.parent.pieceCheck(self.side, self.id, self.x, self.y)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindow()
        self.setFrame()

        #self.board = [[0 for i in range(9)] for j in range(10)]
        self.nboard = None
        self.threadRed = None
        self.threadBlack = None
        self.playerRedIndex = 0
        self.playerBlackIndex = 0
        self.lastMove = []
        self.choosedPiece = []

        self.initial()
        self.show()#启动窗口

        timer = QTimer(self)
        timer.timeout.connect(self.showStat)
        timer.start(100)

    def setWindow(self):
        self.setFixedSize(1000, 800)#设置窗口大小
        self.setWindowTitle('Chinese Chess')#设置窗口标题
    #    self.setWindowIcon(QIcon('icon.png'))#设置窗口图标
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap("img\\background.jpg")))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)

    def setFrame(self):
        self.redLabel = QLabel('红方(先手)：',self)
        self.redPlayer0Button = QRadioButton('玩家', self)  # 单选窗口
        self.redPlayer1Button = QRadioButton('eleeye', self)  # 单选窗口
        self.redPlayer2Button = QRadioButton('丰光南', self)  # 单选窗口
        self.redPlayer3Button = QRadioButton('空', self)  # 单选窗口
        self.redPlayer4Button = QRadioButton('空', self)  # 单选窗口
        self.redPlayer5Button = QRadioButton('空', self)  # 单选窗口
        self.redPlayer6Button = QRadioButton('空', self)  # 单选窗口
        self.group1 = QButtonGroup(self)
        self.group1.setExclusive(True)
        self.group1.addButton(self.redPlayer0Button)
        self.group1.addButton(self.redPlayer1Button)
        self.group1.addButton(self.redPlayer2Button)
        self.group1.addButton(self.redPlayer3Button)
        self.group1.addButton(self.redPlayer4Button)
        self.group1.addButton(self.redPlayer5Button)
        self.group1.addButton(self.redPlayer6Button)
        self.group1.setId(self.redPlayer0Button,0)
        self.group1.setId(self.redPlayer1Button,1)
        self.group1.setId(self.redPlayer2Button,2)
        self.group1.setId(self.redPlayer3Button,3)
        self.group1.setId(self.redPlayer4Button,4)
        self.group1.setId(self.redPlayer5Button,5)
        self.group1.setId(self.redPlayer6Button,6)
        self.redPlayer0Button.setChecked(True)

        self.blackLabel = QLabel('黑方(后手)：',self)
        self.blackPlayer0Button = QRadioButton('玩家', self)  # 单选窗口
        self.blackPlayer1Button = QRadioButton('eleeye', self)  # 单选窗口
        self.blackPlayer2Button = QRadioButton('丰光南', self)  # 单选窗口
        self.blackPlayer3Button = QRadioButton('空', self)  # 单选窗口
        self.blackPlayer4Button = QRadioButton('空', self)  # 单选窗口
        self.blackPlayer5Button = QRadioButton('空', self)  # 单选窗口
        self.blackPlayer6Button = QRadioButton('空', self)  # 单选窗口
        self.group2 = QButtonGroup(self)
        self.group2.setExclusive(True)
        self.group2.addButton(self.blackPlayer0Button)
        self.group2.addButton(self.blackPlayer1Button)
        self.group2.addButton(self.blackPlayer2Button)
        self.group2.addButton(self.blackPlayer3Button)
        self.group2.addButton(self.blackPlayer4Button)
        self.group2.addButton(self.blackPlayer5Button)
        self.group2.addButton(self.blackPlayer6Button)
        self.group2.setId(self.blackPlayer0Button,0)
        self.group2.setId(self.blackPlayer1Button,1)
        self.group2.setId(self.blackPlayer2Button,2)
        self.group2.setId(self.blackPlayer3Button,3)
        self.group2.setId(self.blackPlayer4Button,4)
        self.group2.setId(self.blackPlayer5Button,5)
        self.group2.setId(self.blackPlayer6Button,6)
        self.blackPlayer0Button.setChecked(True)

        self.enableChooseGame = QRadioButton('棋局：',self)#单选窗口
        self.enableChooseGame.clicked.connect(self.enableChoose)
        self.showChooseFile = QLineEdit(self)
        self.showChooseFile.setEnabled(False)
        self.chooseFileButton = QPushButton('选择文件',self)
        self.chooseFileButton.setEnabled(False)
        self.chooseFileButton.clicked.connect(self.chooseFile)
        self.buttonRestart = QPushButton('重新开始', self)#创建重新开始按钮
        self.buttonRestart.clicked.connect(self.initial)
        self.textLabel = QLabel('历史走步:',self)
        self.text = QTextEdit('',self)
        self.text.setReadOnly(True)

        self.buttonRestart.resize(105,35)
        self.buttonRestart.move(172, 478)

        buttonwidth = 200
        buttonHeight = 30
        self.redLabel.resize(buttonwidth, buttonHeight)
        self.blackLabel.resize(buttonwidth, buttonHeight)
        self.enableChooseGame.resize(buttonwidth, buttonHeight)
        self.showChooseFile.resize(buttonwidth, buttonHeight)
        self.chooseFileButton.resize(buttonwidth, buttonHeight)
        self.buttonRestart.resize(buttonwidth, buttonHeight)
        self.textLabel.resize(buttonwidth, buttonHeight)
        self.text.resize(buttonwidth, 5*buttonHeight)

        buttonx = 750

        self.redLabel.move(buttonx, 80)
        self.redPlayer0Button.move(buttonx,110)
        self.redPlayer1Button.move(buttonx + buttonwidth/2,110)
        self.redPlayer2Button.move(buttonx,140)
        self.redPlayer3Button.move(buttonx + buttonwidth/2,140)
        self.redPlayer4Button.move(buttonx,170)
        self.redPlayer5Button.move(buttonx + buttonwidth/2,170)
        self.redPlayer6Button.move(buttonx,200)

        self.blackLabel.move(buttonx, 230)
        self.blackPlayer0Button.move(buttonx,260)
        self.blackPlayer1Button.move(buttonx + buttonwidth/2,260)
        self.blackPlayer2Button.move(buttonx,290)
        self.blackPlayer3Button.move(buttonx + buttonwidth/2,290)
        self.blackPlayer4Button.move(buttonx,320)
        self.blackPlayer5Button.move(buttonx + buttonwidth/2,320)
        self.blackPlayer6Button.move(buttonx,350)

        self.enableChooseGame.move(buttonx, 380)
        self.showChooseFile.move(buttonx, 410)
        self.chooseFileButton.move(buttonx, 440)
        self.buttonRestart.move(buttonx, 500)
        self.textLabel.move(buttonx,530)
        self.text.move(buttonx, 560)


        self.pieces = []
        for i in range(10):
            self.pieceRow = []
            for j in range(9):
                self.temp = piece(None,None, j, 9-i, self)
                self.temp.resize(70, 70)
                x_s, y_s = self._pos_to_screen(j, 9-i)
                self.temp.move(x_s, y_s)
                self.pieceRow.append(self.temp)
            self.pieces.append(self.pieceRow)

    def initial(self):
        self.stopping = 1
        if self.threadRed:
            if self.playerRedIndex == 1:
                self.playerRed.quit()
                self.playerRed.join()
            self.threadRed.quit()
            self.threadRed.join()

        if self.threadBlack:
            if self.playerBlackIndex == 1:
                self.playerBlack.quit()
                self.playerBlack.join()
            self.threadBlack.quit()
            self.threadBlack.join()

        self.side = 0
        self.moving = 0
        self.stopping = 0
        self.finish = 0
        self.stepQueue = Queue()
        self.lastMove = []
        self.choosedPiece = []
        self.playerRedIndex = self.group1.checkedId()
        self.playerBlackIndex = self.group2.checkedId()
        self.text.setText("")


        if self.enableChooseGame.isChecked():
            text_str = self.showChooseFile.text().strip()
            if text_str == '':
                QMessageBox.warning(self, "Warning", "请输入文件名")
                return
            else:
                try:
                    game = read_from_xqf(text_str)
                    for key in game.info:
                        if type(game.info[key]) == type('sample'):
                            self.text.append(key+" "+game.info[key])
                        else:
                            temp = key + " " + str(game.info[key])
                            self.text.append(temp)
                    self.nboard = ChessBoard(game.init_board.to_fen())
                except:
                    QMessageBox.warning(self, "Warning", "没有此的文件")
                    return
        else:
            self.nboard = ChessBoard(FULL_INIT_FEN)
        self.board = self.nboard.get_board()[::-1]

        ch_set = ['k', 'a', 'b', 'n', 'r', 'c', 'p']
        for i in range(10):
            for j in range(9):
                self.pieces[i][j].id = self.board[i][j]
                if self.board[i][j]:
                    if self.board[i][j] in ch_set:
                        self.pieces[i][j].side = 1
                    else:
                        self.pieces[i][j].side = 0
                    self.pieces[i][j].setStyleSheet("background-image:url(\"img/" + self.board[i][j] + str(self.pieces[i][j].side) + ".png\");border:0")
                else:
                    self.pieces[i][j].side = None
                    self.pieces[i][j].setStyleSheet("background-image:none;border:0")

        self.text.append("·红方执棋...")

        if self.playerRedIndex == 0:
            self.playerRed = None
        elif self.playerRedIndex == 1:
            self.playerRed = UcciEngine()
            self.playerRed.load("cchess2/test/eleeye/eleeye.exe")
        elif self.playerRedIndex == 2:
            self.playerRed = abpa_fgn.Abpa(True)
        else:
            self.playerRed = None

        if self.playerBlackIndex == 0:
            self.playerBlack = None
        elif self.playerBlackIndex == 1:
            self.playerBlack = UcciEngine()
            self.playerBlack.load("cchess2/test/eleeye/eleeye.exe")
        elif self.playerBlackIndex == 2:
            self.playerBlack = abpa_fgn.Abpa(False)
        else:
            self.playerBlack = None

        if self.playerRedIndex != 0:
            self.threadRed = myThread(0,self.aiMove)
            self.threadRed.start()
        else:
            self.threadRed = None
        if self.playerBlackIndex !=0:
            self.threadBlack = myThread(1,self.aiMove)
            self.threadBlack.start()
        else:
            self.threadBlack = None

    def eleeyeEngine(self,engine):
        while True:
            engine.handle_msg_once()
            if engine.move_queue.empty():
                time.sleep(0.2)
                continue
            output = engine.move_queue.get()
            if output[0] == 'best_move':
                p_from, p_to = output[1]["move"]
                return [p_from.x, p_from.y, p_to.x, p_to.y]
            elif output[0] == 'info_move':
                continue
            elif output[0] == 'dead':
                return -1
            elif output[0] == 'draw':
                return 0
            elif output[0] == 'resign':
                return 1

    def _move(self, xfrom, yfrom, xto, yto):
        move = self.nboard.move(Pos(xfrom, yfrom), Pos(xto, yto))
        if move is None:
            return None
        self.nboard.next_turn()
        self.lastMove = [xfrom,yfrom,xto,yto]

        lock2.acquire()
        self.stepQueue.put(move.to_chinese())
        if self.nboard.is_checkmate():
            self.finish = 1
            self.stepQueue.put("*将死，" + {0:"红方",1:"黑方"}[self.side] + "胜")
        else:
            self.stepQueue.put({1: '· 红方执棋...', 0: '· 黑方执棋...'}[self.side])
        lock2.release()
        self.pieces[9-yto][xto].id = self.pieces[9-yfrom][xfrom].id
        self.pieces[9-yto][xto].side = self.pieces[9-yfrom][xfrom].side
        self.pieces[9-yfrom][xfrom].id = None
        self.pieces[9-yfrom][xfrom].side = None
        self.pieces[9-yfrom][xfrom].setStyleSheet("background-image:url();border:0")
        if self.pieces[9-yto][xto].side == 0:
            self.pieces[9-yto][xto].setStyleSheet("background-image:url(\"img/"+self.pieces[9-yto][xto].id + str(self.pieces[9-yto][xto].side) +".png\");border:0")
        else:
            self.pieces[9-yto][xto].setStyleSheet("background-image:url(\"img/"+self.pieces[9-yto][xto].id + str(self.pieces[9-yto][xto].side) +".png\");border:0")

        self.side = {0: 1, 1: 0}[self.side]
        return 1

    def showStat(self):
        lock2.acquire()
        if not self.stepQueue.empty():
            self.text.append(self.stepQueue.get())
        lock2.release()

    def aiMove(self,side):
        if not (self.finish == 1 or self.side != side or self.stopping == 1):
            if side  == 0 and self.playerRedIndex > 0:
                if self.playerRedIndex == 1:
                    self.playerRed.go_from(self.nboard.to_fen(), 8)
                    l = self.eleeyeEngine(self.playerRed)
                    if l in [-1,0,1]:
                        print("terminate")
                        self.finish = 1
                    else:
                        (xfrom, yfrom, xto, yto) = l
                        self._move(xfrom,yfrom,xto,yto)
                else:
                    if len(self.lastMove) != 0:
                        self.playerRed.opponentMove(self.lastMove[1],self.lastMove[0],self.lastMove[3],self.lastMove[2])
                    yfrom, xfrom, yto, xto = self.playerRed.myStep()
                    if self.playerRed.iWin:
                        self.finish = 1
                        print("AI Red feel it Win")
                    else:
                        self._move(xfrom, yfrom, xto, yto )
            elif side == 1 and self.playerBlackIndex > 0:
                if self.playerBlackIndex == 1:
                    self.playerBlack.go_from(self.nboard.to_fen(), 8)
                    l = self.eleeyeEngine(self.playerBlack)
                    if l in [-1,0,1]:
                        print("terminate")
                        self.finish = 1
                    else:
                        (xfrom, yfrom, xto, yto) = l
                        self._move(xfrom,yfrom,xto,yto)
                else:
                    if len(self.lastMove) != 0:
                        self.playerBlack.opponentMove(self.lastMove[1],self.lastMove[0],self.lastMove[3],self.lastMove[2])
                    yfrom, xfrom, yto, xto = self.playerBlack.myStep()
                    if self.playerBlack.iWin:
                        self.finish = 1
                        print("AI Black feel it Win")
                    else:
                        self._move(xfrom, yfrom, xto, yto )

    def pieceCheck(self,side,id,x,y):
        if self.finish == 1 or (self.side == 0 and self.playerRedIndex > 0) or (self.side == 1 and self.playerBlackIndex > 0):
            return
        if self.moving == 0:
            if side == self.side:
                self.moving = 1
                self.choosedPiece = [side,x,y]
        else:
            sidefrom = self.choosedPiece[0]
            xfrom = self.choosedPiece[1]
            yfrom = self.choosedPiece[2]
            if sidefrom == side:
                self.choosedPiece = [side, x, y]
            else:
                if self._move(xfrom,yfrom,x,y):
                    self.moving = 0
                else:
                    print("invalid move")

    def enableChoose(self):
        self.showChooseFile.setEnabled(self.enableChooseGame.isChecked())
        self.chooseFileButton.setEnabled(self.enableChooseGame.isChecked())
        pass

    def chooseFile(self):
        text_str,_ = QFileDialog().getOpenFileName(self)
        self.showChooseFile.setText(text_str)

    def _pos_to_screen(self, x, y):
        x_s = 55 + x * 70
        y_s = 55 + 70 * 9 - y * 70
        return x_s, y_s

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())