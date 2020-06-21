# Author : Kelvin
# Date : 2019/2/3 21:51
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socket
import threading
import time
import sys

class TcpSever(QThread):
    # 定义信号,定义参数为str类型
    recvmsg_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    #发送消息槽函数
    def sendMsg(self, sendMsg):
        self.client_socket.send(sendMsg.encode(encoding="utf-8"))

    # 接收消息
    def __client_thread(self, client_socket, ip_port, recvmsg_signal):
        while True:
            try:
                #该接收方式应该为阻塞接收方式
                recvMsg = client_socket.recv(2048)
                # 如果接收的消息长度不为0，则将其解码输出
            except: #TODO:这里应该需要抓取客户端断开连接的异常
                pass
            else:
                if recvMsg:
                    print("[客户端消息]", ip_port, ":", recvMsg.decode("utf-8"))
                    recvmsg_signal.emit(recvMsg.decode("gbk"))
                else:
                    print("客户端", ip_port, "已下线")

    def create(self, server_addr, port):
        self.server_addr = server_addr
        self.port = port
        # 创建TCP套接字
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口复用
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    def run(self):
        # 绑定端口
        self.tcp_socket.bind((self.server_addr, self.port))
        # 设置为被动监听状态，128表示最大连接数
        self.tcp_socket.listen(128)
        self.clientList = []
        while True:
            # 等待客户端连接
            self.client_socket, ip_port = self.tcp_socket.accept()
            self.clientList.append(self.client_socket)
            print("[新客户端]:", ip_port, "已连接")
            self.client_socket.setblocking(False)    # 将套接字设置为非堵塞　
            # 有客户端连接后，创建一个线程将客户端套接字，IP端口传入recv函数，
            t1 = threading.Thread(target=self.__client_thread, args=(self.client_socket, ip_port, self.recvmsg_signal))
            # 设置线程守护
            t1.setDaemon(True)
            # 启动线程
            t1.start()

    def close(self):
        for client_fd in self.clientList:
            client_fd.close()
        self.tcp_socket.close()

if __name__ == "__main__":
    tcp_sever = TcpSever()
    tcp_sever.create("192.168.100.102", 5000)
    tcp_sever.run()