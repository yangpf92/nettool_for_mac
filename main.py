import sys
#import MainWindow
from MainWindow import *
from PyQt5.QtWidgets import QApplication,QMainWindow

#  连接按钮槽函数
def buttonNetConnect_slot(self):
    print("buttonNetConnect_slot")


def set_signal_slot(self):
    ui.buttonNetConnect.clicked.connect(buttonNetConnect_slot)


#不是在函数和类中定义的变量相当于全局变量，所以上方可以直接使用
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 初始化app
    mainwindow = QMainWindow()  # 创建主窗口
    ui = Ui_MainWindow()  # 创建UI界面
    ui.setupUi(mainwindow)  # 初始化UI到主窗口，主要是建立代码与ui之间的signal与slot
    set_signal_slot(ui)
    mainwindow.show()  # 显示窗口
    sys.exit(app.exec_())  # 消息循环结束之后返回0，接着调用sys.exit(0)退出程序