import sys
#import MainWindow
from MainWindow import *
from PyQt5.QtWidgets import QApplication,QMainWindow
from deviceinfo import DeviceInfo
from tcpserver import TcpSever
import threading

class NetToolWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetTool")
        self.setupUi(self)
        self.__show_ipaddr()
        self.buttonNetConnect_state = False
        self.send_msg = ""

    ##########槽函数
    def __showMsg_sloat(self, recv_msg):
        self.textBrowserNetRecv.insertPlainText(recv_msg+'\n')

    def __show_connect_tcpClient_info(self, client_connect_info):
        #TODO: 返回的客户端列表的格式为('192.168.50.3', 39584)  我们需要对字符串进行切片，去掉括号，以及ip地址左右的单引号
        client_connect_info_tuple = tuple(client_connect_info.split(","))
        print(client_connect_info_tuple[0][2:-1] + ":" + client_connect_info_tuple[1][:-1])
        self.comboBoxConnectClientList.addItem(client_connect_info_tuple[0][2:-1] + ":" + client_connect_info_tuple[1][1:-1])

    def __butonSend_slot(self):
        if self.buttonNetConnect_state == True:
            if self.textEditNetSend.document().isEmpty():
                pass
            else:
                client_tuple = tuple(self.comboBoxConnectClientList.currentText().split(":"))
                self.tcp_server.sendMsg(client_tuple, self.textEditNetSend.toPlainText())
                #print(self.textEditNetSend.toPlainText())

    def __buttonNetConnect_slot(self):
        if len(self.lineEditNetPort.text()) == 0:
            print("network port is  empety")
            return
        else:
            print("1111111")
        print("__buttonNetConnect_slot")

        #改变connect button的值
        if self.buttonNetConnect_state == False :
            print(str(sys._getframe().f_lineno) + "=============")
            #修改界面元素属性
            self.buttonNetConnect.setText("断开连接")
            self.lineEditNetPort.setReadOnly(True)  #设置只读
            #self.lineEditNetPort.setFocusPolicy(False)


            # 创建一个tcp线程
            self.tcpserver_t = threading.Thread(target=self.__tcpserver_thread_cb, args=(
            self.comboBoxNetConnectAddr.currentText(), int(self.lineEditNetPort.text())))
            self.tcpserver_t.start()
            #更新状态标志
            self.buttonNetConnect_state = True
        else:
            print(str(sys._getframe().f_lineno) + "=============")
            self.tcp_server.close()
            #更新状态标志
            self.buttonNetConnect_state = False

            #更新页面元素
            self.buttonNetConnect.setText("开始连接")
            self.comboBoxConnectClientList.clear()  #清空连接列表

    def __buttonClearRecvBuffer_sloat(self):
        self.textBrowserNetRecv.clear()

    def __buttonClearSendBuffer_sloat(self):
        self.textEditNetSend.clear()

    # 添加信号与槽
    def add_signal_slot(self):
        self.buttonSend.clicked.connect(self.__butonSend_slot)
        self.buttonNetConnect.clicked.connect(self.__buttonNetConnect_slot)
        self.buttonClearRecvBuffer.clicked.connect(self.__buttonClearRecvBuffer_sloat)
        self.buttonClearSendBuffer.clicked.connect(self.__buttonClearSendBuffer_sloat)

    #客户端连接列表展示
    def __showConnect_clientAddr(self, connect_client_addr):
        self.comboBoxConnectClientList.addItem(connect_client_addr)

    #重写关闭窗口事件
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        try:
            self.tcp_server.close()
        except:
            pass
        else:
            pass

    def __show_ipaddr(self):
        deviceinfo = DeviceInfo()
        deviceinfo.get_host_info()
        deviceinfo.get_interface_info()
        deviceinfo.show()
        for ipaddr in deviceinfo.ipaddr_list:
            self.comboBoxNetConnectAddr.addItem(ipaddr)

    def __tcpserver_thread_cb(self, ipaddr, port):
        self.tcp_server = TcpSever()
        self.tcp_server.recvmsg_signal.connect(self.__showMsg_sloat)
        self.tcp_server.clientInfo_signal.connect(self.__show_connect_tcpClient_info)
        self.tcp_server.create(ipaddr, port)    #添加tcp接收槽函数
        self.tcp_server.run()

#不是在函数和类中定义的变量相当于全局变量，所以上方可以直接使用
if __name__ == '__main__':
    app = QApplication(sys.argv)
    nettool_window = NetToolWindow()
    nettool_window.add_signal_slot()
    nettool_window.setWindowTitle("netTools")
    nettool_window.show()
    sys.exit(app.exec_())