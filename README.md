# 接口说明
- 实现使用abpa+姓名首字母的形式作为文件名，例如：`abpaFgn.py`作为文件名
- 上述文件下实现一个名为`Abpa()`的类，界面在启动时调用它的构造函数，构造函数中没有任何参数
- 类中需要实现如下接口：
    - 构造函数，仅有一个参数表示自己是不是“下面”的那一方，“下面”的定义见后文
    ```python
    def __init__(self, down = True)
    ```
    - 返回自己的走步，把位于(fromX, fromY)的棋子移动到(toX, toY)
    ```python
    def myStep()
        #TODO
        return (fromX, fromY, toX, toY)
    ```
    - 传入对手的走步
    ```python
    def opponentMove(fromX, fromY, toX, toY)
        #TODO
    ```
    - 表示自己是否胜利，`iWin = False`
    应在构造函数中置为False，当胜利时置为True，UI每调用一次move就会检查一次该变量，UI层大致的代码框架如下：
    ```python
    a = abpaFgn.Abpa(down = True)
    b = abpaDjh.Abpa(down = False)
    #画图
    (fromX, fromY, toX, toY) = b.myMove()
    while True:
        a.opponentMove(fromX, fromY, toX, toY)
        (fromX, fromY, toX, toY) = a.myStep()
        #画图
        if a.iWin == True:
            break
        b.opponentMove(fromX, fromY, toX, toY)
        (fromX, fromY, toX, toY) = b.myMove()
        #画图
        if b.iWin == True:
            break
    ```
- 棋盘规定坐标编号如下
```
| (9, 0) | (9, 1) | (9, 2) | (9, 3) | (9, 4) | (9, 5) | (9, 6) | (9, 7) | (9, 8) |
| (8, 0) | (8, 1) | (8, 2) | (8, 3) | (8, 4) | (8, 5) | (8, 6) | (8, 7) | (8, 8) |
| (7, 0) | (7, 1) | (7, 2) | (7, 3) | (7, 4) | (7, 5) | (7, 6) | (7, 7) | (7, 8) |
| (6, 0) | (6, 1) | (6, 2) | (6, 3) | (6, 4) | (6, 5) | (6, 6) | (6, 7) | (6, 8) |
| (5, 0) | (5, 1) | (5, 2) | (5, 3) | (5, 4) | (5, 5) | (5, 6) | (5, 7) | (5, 8) |
| (4, 0) | (4, 1) | (4, 2) | (4, 3) | (4, 4) | (4, 5) | (4, 6) | (4, 7) | (4, 8) |
| (3, 0) | (3, 1) | (3, 2) | (3, 3) | (3, 4) | (3, 5) | (3, 6) | (3, 7) | (3, 8) |
| (2, 0) | (2, 1) | (2, 2) | (2, 3) | (2, 4) | (2, 5) | (2, 6) | (2, 7) | (2, 8) |
| (1, 0) | (1, 1) | (1, 2) | (1, 3) | (1, 4) | (1, 5) | (1, 6) | (1, 7) | (1, 8) |
| (0, 0) | (0, 1) | (0, 2) | (0, 3) | (0, 4) | (0, 5) | (0, 6) | (0, 7) | (0, 8) |
```
- 棋盘棋子参考
```
车 马 象 士 帅 士 象 马 车
+  +  +  +  +  +  +  +  +
+  炮 +  +  +  +  +  炮 +
卒 +  卒 +  卒 +  卒 +  卒
+  +  +  +  +  +  +  +  +
+  +  +  +  +  +  +  +  +
+  +  +  +  +  +  +  +  +
+  炮 +  +  +  +  +  炮 +
+  +  +  +  +  +  +  +  +
车 马 象 士 帅 士 象 马 车
```
- **基于前面的编号和棋子参考，这里定义的“下面”是拥有0~4行的棋子**
- 如果需要写成多个程序文件，请将其他文件放在命名形如`libFgn`的文件夹里
- UI层不提供任何数据结构上的支持，如不能通过UI层来获取某个位置上是什么棋子
- **调用界面对棋局不作任的合法性判断，如胜负、某个位置是否有棋子等，也不作检测，也就是说，如果返回值指定的位置没有棋子是会报错的，如果返回值是一个违法的走步，是不会报错的，但可能导致对手的程序崩溃**

<meta http-equiv="refresh" content="1">
