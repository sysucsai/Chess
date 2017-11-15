import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

'''
在这里import你们的文件！！！！！！！！！！！！！！！！！！！！！！！！！
'''
import abpa_fgn



class piece(QLabel):
    def __init__(self, id, x, y, parent):
        super(QLabel, self).__init__(parent)
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y

    def mousePressEvent(self, QMouseEvent):
        self.parent.pieceCheck(self.id, self.x, self.y)


class Window(QWidget):
    def __init__(self):
        super().__init__()#调用父构造函数初始化
        self.setWindow()#设置窗口
        self.setBackground()#初始化背景
        self.setFrame()#设置按钮
        self.board = [[0 for i in range(9)] for j in range(10)]

        '''
        在这里添加你们的引擎！！！！！！！！！！！！！！！！！！！！！！！
        然后就没有了，在界面选择自己的引擎
        '''
        self.index_to_play = {
            0: 0,
            1: 0,
            2: abpa_fgn.Abpa(),
            3: 0,
            4: 0,
            5: 0,
            6: 0
        }

        self.finish = 0
        self.moving = 0
        self.side = 0
        self.playerRed = 0
        self.playerBlack = 0
        self.lastMove = []
        self.choosedPiece = []
        self.initial()
        self.show()#启动窗口

    def setWindow(self):
        self.setFixedSize(1000, 800)#设置窗口大小
        self.setWindowTitle('Chinese Chess')#设置窗口标题
    #    self.setWindowIcon(QIcon('icon.png'))#设置窗口图标

    def setBackground(self):
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap("img\\background.jpg")))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)

    def setFrame(self):
        self.redLabel = QLabel('红方：',self)
        self.redChoose = QComboBox(self)
        self.redChoose.addItem("0")
        self.redChoose.addItem("1")
        self.redChoose.addItem("2")
        self.redChoose.addItem("3")
        self.redChoose.addItem("4")
        self.redChoose.addItem("5")
        self.redChoose.addItem("6")
        self.blackLabel = QLabel('黑方：',self)
        self.blackChoose = QComboBox(self)
        self.blackChoose.addItem("0")
        self.blackChoose.addItem("1")
        self.blackChoose.addItem("2")
        self.blackChoose.addItem("3")
        self.blackChoose.addItem("4")
        self.blackChoose.addItem("5")
        self.blackChoose.addItem("6")
        self.enableChooseGame = QRadioButton('棋局：',self)#单选窗口
        self.showChooseFile = QLineEdit(self)
        self.showChooseFile.setEnabled(False)
        self.chooseFileButton = QPushButton('选择文件',self)
        self.chooseFileButton.setEnabled(False)
        self.buttonRestart = QPushButton('重新开始', self)#创建重新开始按钮
        self.buttonRestart.clicked.connect(self.initial)#开始游戏
        #self.buttonRestart.setStyleSheet("border: none;font-family:微软雅黑;font-size:15px")
        self.textLabel = QLabel('历史走步:',self)
        #self.player2.setAlignment(Qt.AlignCenter)
        #self.player2.setStyleSheet("font-family:微软雅黑;font-size:25px")
        self.text = QTextEdit('',self)
        self.text.setReadOnly(True)

        self.buttonRestart.resize(105,35)
        self.buttonRestart.move(172, 478)

        buttonwidth = 200
        buttonHeight = 30
        self.redLabel.resize(buttonwidth, buttonHeight)
        self.redChoose.resize(buttonwidth, buttonHeight)
        self.blackLabel.resize(buttonwidth, buttonHeight)
        self.blackChoose.resize(buttonwidth, buttonHeight)
        self.enableChooseGame.resize(buttonwidth, buttonHeight)
        self.showChooseFile.resize(buttonwidth, buttonHeight)
        self.chooseFileButton.resize(buttonwidth, buttonHeight)
        self.buttonRestart.resize(buttonwidth, buttonHeight)
        self.textLabel.resize(buttonwidth, buttonHeight)
        self.text.resize(buttonwidth, 5*buttonHeight)

        buttonx = 750

        self.redLabel.move(buttonx, 80)
        self.redChoose.move(buttonx, 110)
        self.blackLabel.move(buttonx, 140)
        self.blackChoose.move(buttonx, 170)
        self.enableChooseGame.move(buttonx, 200)
        self.showChooseFile.move(buttonx, 230)
        self.chooseFileButton.move(buttonx, 260)
        self.buttonRestart.move(buttonx, 320)
        self.textLabel.move(buttonx,400)
        self.text.move(buttonx, 430)

        '''
        '''
        self.pieces = []
        for i in range(10):
            self.pieceRow = []
            for j in range(9):
                x_s, y_s = self._pos_to_screen(j, i)
                self.temp = piece(0,i, j, self)
                self.temp.move(x_s, y_s)
                self.temp.resize(70, 70)
                #self.temp.setVisible(False)
                #self.temp.setEnabled(False)
                self.pieceRow.append(self.temp)
            self.pieces.append(self.pieceRow)


    def initial(self):
        if self.enableChooseGame.isChecked() and strip(self.showChooseFile.text()) != '':
            pass
        else:
            self.board[0][0] = 15
            self.board[0][1] = 14
            self.board[0][2] = 13
            self.board[0][3] = 12
            self.board[0][4] = 11
            self.board[0][5] = 12
            self.board[0][6] = 13
            self.board[0][7] = 14
            self.board[0][8] = 15
            self.board[2][1] = 16
            self.board[2][7] = 16
            self.board[3][0] = 17
            self.board[3][2] = 17
            self.board[3][4] = 17
            self.board[3][6] = 17
            self.board[3][8] = 17

            self.board[9][0] = 25
            self.board[9][1] = 24
            self.board[9][2] = 23
            self.board[9][3] = 22
            self.board[9][4] = 21
            self.board[9][5] = 22
            self.board[9][6] = 23
            self.board[9][7] = 24
            self.board[9][8] = 25
            self.board[7][1] = 26
            self.board[7][7] = 26
            self.board[6][0] = 27
            self.board[6][2] = 27
            self.board[6][4] = 27
            self.board[6][6] = 27
            self.board[6][8] = 27
        pass

        for i in range(10):
            for j in range(9):
                self.pieces[i][j].id = self.board[i][j]
                if self.board[i][j] != 0:
                    if self.board[i][j]//10 == 2:
                        self.pieces[i][j].setStyleSheet("background-image:url(\"img/b"+str(self.board[i][j]%10)+".png\");border:0")
                    else:
                        self.pieces[i][j].setStyleSheet("background-image:url(\"img/r"+str(self.board[i][j]%10)+".png\");border:0")
                else:
                    self.pieces[i][j].setStyleSheet("background-image:none;border:0")

        self.side = 0
        self.moving = 0
        self.finish = 0
        self.lastMove = []
        self.choosedPiece = []
        self.playerRed = self.index_to_play[self.redChoose.currentIndex()]
        self.playerBlack = self.index_to_play[self.blackChoose.currentIndex()]
        print(self.redChoose.currentText(), "vs", self.blackChoose.currentText())

        while(self.side == 1 and self.playerRed != 0) or (self.side == 0 and self.playerBlack != 0):
            if self.side == 1 and self.playerRed != 0:
                print("bug1")
                if len(self.lastMove) != 0:
                    self.playerRed.opponentMove(9 - self.lastMove[0],self.lastMove[1],9 - self.lastMove[2],self.lastMove[3])
                cx,cy,nx,ny = self.playerRed.myStep()
                if self.playerRed.iWin:
                    self.finish == 1
                    print("Player Red Win")
                    return
                else:
                    print("bug2")
                    self._move(9 - cx,cy,9 - nx,ny)
                    self.side = {0:1,1:0}[self.side]
                    return
            if self.side == 0 and self.playerBlack != 0:
                print("bug11")
                if len(self.lastMove) != 0:
                    self.playerBlack.opponentMove(9 - self.lastMove[0],self.lastMove[1],9 - self.lastMove[2],self.lastMove[3])
                cx,cy,nx,ny = self.playerBlack.myStep()
                if self.playerBlack.iWin:
                    self.finish == 1
                    print("Player Black Win")
                    return
                else:
                    print("bug22")
                    self._move(9 - cx,cy,9 - nx,ny)
                    self.side = {0:1,1:0}[self.side]
                    return


    def _move(self,cx,cy,x,y):
        eat = 0
        if self.pieces[x][y].id != 0:
            eat = 1
        temp = self.pieces[cx][cy]
        self.pieces[cx][cy] = self.pieces[x][y]
        self.pieces[x][y] = temp

        self.pieces[x][y].x = x
        self.pieces[x][y].y = y
        x_s, y_s = self._pos_to_screen(y, x)
        self.pieces[x][y].move(x_s, y_s)

        self.pieces[cx][cy].x = cx
        self.pieces[cx][cy].y = cy
        cx_s, cy_s = self._pos_to_screen(cy, cx)
        self.pieces[cx][cy].move(cx_s, cy_s)
        if eat:
            self.pieces[cx][cy].id = 0
            self.pieces[cx][cy].setStyleSheet("background-image:none;border:0")
        self.lastMove = [cx,cy,x,y]

    def pieceCheck(self,id,x,y):
        if self.finish == 1:
            return
        print(self.side)
        if self.moving == 0:
            if id == 0:
                print("这里什么都没有啊....")
                return
            self.moving = 1
            self.choosedPiece = [id,x,y]
            return
        else:
            cid = self.choosedPiece[0]
            cx = self.choosedPiece[1]
            cy = self.choosedPiece[2]
            if cid//10 == id//10:
                self.choosedPiece = [id, x, y]
                return
            else:
                self._move(cx,cy,x,y)
                self.moving = 0
                self.side = {0:1,1:0}[self.side]

        if self.side == 1 and self.playerRed != 0:
            print("bug1")
            self.playerRed.opponentMove(9 - self.lastMove[0],self.lastMove[1],9 - self.lastMove[2],self.lastMove[3])
            cx,cy,nx,ny = self.playerRed.myStep()
            if self.playerRed.iWin:
                self.finish == 1
                print("Player Red Win")
                return
            else:
                print("bug2")
                self._move(9 - cx,cy,9 - nx,ny)
                self.side = {0:1,1:0}[self.side]
                return
        if self.side == 0 and self.playerBlack != 0:
            print("bug11")
            self.playerBlack.opponentMove(9 - self.lastMove[0],self.lastMove[1],9 - self.lastMove[2],self.lastMove[3])
            cx,cy,nx,ny = self.playerBlack.myStep()
            if self.playerBlack.iWin:
                self.finish == 1
                print("Player Black Win")
                return
            else:
                print("bug22")
                self._move(9 - cx,cy,9 - nx,ny)
                self.side = {0:1,1:0}[self.side]
                return


    def _pos_to_screen(self, x, y):
        x_s = 55 + x * 70
        y_s = 55 + y * 70
        return x_s, y_s

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())