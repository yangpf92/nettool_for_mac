import sys
#import MainWindow
from MainWindow import *
from PyQt5.QtWidgets import QApplication,QMainWindow
from deviceinfo import DeviceInfo
from tcpserver import TcpSever
import threading

#  连接按钮槽函数


class NetToolWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetTool")
        self.setupUi(self)
        self.__show_ipaddr()
        self.buttonNetConnect_state = False
        self.send_msg = ""

    def __showMsg_sloat(self, recv_msg):
        self.textBrowserNetRecv.insertPlainText(recv_msg+'\n')

    #重写关闭窗口事件
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.tcp_server.close()

    def __show_ipaddr(self):
        deviceinfo = DeviceInfo()
        deviceinfo.get_host_info()
        deviceinfo.get_interface_info()
        deviceinfo.show()
        for ipaddr in deviceinfo.ipaddr_list:
            self.comboBoxNetConnectAddr.addItem(ipaddr)

    #添加信号与槽
    def add_signal_slot(self):
        self.buttonSend.clicked.connect(self.__butonSend_slot)
        self.buttonNetConnect.clicked.connect(self.__buttonNetConnect_slot)

    def __butonSend_slot(self):
        if self.buttonNetConnect_state == True:
            if self.textEditNetSend.document().isEmpty():
                pass
            else:
                self.tcp_server.sendMsg(self.textEditNetSend.toPlainText())
                print(self.textEditNetSend.toPlainText())

    def __buttonNetConnect_slot(self):
        if len(self.lineEditNetPort.text()) == 0:
            print("network port is  empety")
        else:
            print("1111111")
        print("__buttonNetConnect_slot")

        #改变connect button的值
        if self.buttonNetConnect_state == False :
            self.buttonNetConnect.setText("断开连接")
            # 创建一个tcp线程
            self.tcpserver_t = threading.Thread(target=self.__tcpserver_thread_cb, args=(
            self.comboBoxNetConnectAddr.currentText(), int(self.lineEditNetPort.text())))
            self.tcpserver_t.start()
            #更新状态标志
            self.buttonNetConnect_state = True
        else:
            self.tcp_server.close()
            self.buttonNetConnect.setText("开始连接")
            #更新状态标志
            self.buttonNetConnect_state = False

    def __tcpserver_thread_cb(self, ipaddr, port):
        self.tcp_server = TcpSever()
        self.tcp_server.recvmsg_signal.connect(self.__showMsg_sloat)
        self.tcp_server.create(ipaddr, port)    #添加tcp接收槽函数
        self.tcp_server.run()

#不是在函数和类中定义的变量相当于全局变量，所以上方可以直接使用
if __name__ == '__main__':
    app = QApplication(sys.argv)
    nettool_window = NetToolWindow()
    nettool_window.add_signal_slot()
    nettool_window.show()
    sys.exit(app.exec_())