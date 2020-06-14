import sys
#import MainWindow
from MainWindow import *
from PyQt5.QtWidgets import QApplication,QMainWindow
from deviceinfo import DeviceInfo
#from tcpserver import TcpSever
import threading

#  连接按钮槽函数


class NetToolWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetTool")
        self.setupUi(self)
        self.__show_ipaddr()
        self.buttonNetConnect_state = False

    def __show_ipaddr(self):
        deviceinfo = DeviceInfo()
        deviceinfo.get_host_info()
        deviceinfo.get_interface_info()
        deviceinfo.show()
        for ipaddr in deviceinfo.ipaddr_list:
            self.comboBoxNetConnectAddr.addItem(ipaddr)

    #添加信号与槽
    def add_signal_slot(self):
        self.buttonNetConnect.clicked.connect(self.__buttonNetConnect_slot)

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
            tcpserver_t = threading.Thread(target=self.__tcpserver_thread_cb, args=(
            self.comboBoxNetConnectAddr.currentText(), int(self.lineEditNetPort.text())))
            tcpserver_t.start()
            #更新状态标志
            self.buttonNetConnect_state = True
        else:
            self.tcp_server.sock.server_close()
            self.buttonNetConnect.setText("开始连接")
            #更新状态标志
            self.buttonNetConnect_state = False

    def __tcpserver_thread_cb(self, ipaddr, port):
        from tcpserver import TcpSever
        self.tcp_server = TcpSever()
        self.tcp_server.create(self, ipaddr, port)
        self.tcp_server.run()

#不是在函数和类中定义的变量相当于全局变量，所以上方可以直接使用
if __name__ == '__main__':
    app = QApplication(sys.argv)
    nettool_window = NetToolWindow()
    nettool_window.add_signal_slot()
    nettool_window.show()
    sys.exit(app.exec_())