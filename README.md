# 接口说明
- 实现使用abpa+姓名首字母的形式作为文件名，例如：`abpaFgn.py`作为文件名
- 上述文件下实现一个名为`Abpa()`的类，界面在启动时调用它的构造函数，构造函数中没有任何参数
- 类中需要实现如下接口：
    - 当先手时调用，返回第一步的走步，把位于(fromX, fromY)的棋子移动到(toX, toY)
    ```python
    def firstStep()
        #TODO
        return (fromX, fromY, toX, toY)
    ```
    - 传入对手的走步，返回自己的走步
    ```python
    def move(fromX, fromY, toX, toY)
        #TODO
        return (fromX, fromY, toX, toY)
    ```
    - 表示自己是否胜利，`iWin = False`
    应在构造函数中置为False，当胜利时置为True，UI每调用一次move就会检查一次该变量，UI层大致的代码框架如下：
    ```python
    a = abpaFgn.Abpa()
    b = abpaDjn.Abpa()
    (fromX, fromY, toX, toY) = a.firstStep()
    #画图
    while True:
        (fromX, fromY, toX, toY) = b.firstStep(fromX, fromY, toX, toY)
        #画图
        if b.iWin == True:
            break
        (fromX, fromY, toX, toY) = a.firstStep(fromX, fromY, toX, toY)
        #画图
        if a.iWin == True:
            break
    ```

- 如果需要写成多个程序文件，请将其他文件放在命名形如`libFgn`的文件夹里
- UI层不提供任何数据结构上的支持，如不能通过UI层来获取某个位置上是什么棋子
- **调用界面对棋局不作任的合法性判断，如胜负、某个位置是否有棋子等，也不作检测，也就是说，如果返回值指定的位置没有棋子是会报错的，如果返回值是一个违法的走步，是不会报错的，但可能导致对手的程序崩溃**


<meta http-equiv="refresh" content="1">