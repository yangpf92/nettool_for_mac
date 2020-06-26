# Author : Kelvin
# Date : 2019/2/3 21:51
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socket
import threading
from tools import *
import time
import sys

class TcpSever(QThread):
    #定义常量
    CLIENT_INFO_TIMER_VAL = 5

    # 定义信号
    recvmsg_signal = pyqtSignal(str)
    clientInfo_signal = pyqtSignal(str)

    __disconnect_flag = False
    recv_format = "Ascii"
    send_format = "Ascii"

    def __init__(self, parent=None):
        super().__init__(parent)

    #发送消息槽函数
    def sendMsg(self, client_tupe, sendMsg):
        '''这里的client格式为ip地址+端口号的方式，该函数会在所有连接的客户端中去匹配查找 传递下来的格式为[192.168.50.3:39604]
        '''
        for client_node in self.__clientList:
            if str(client_node.getpeername()).find(str(client_tupe[0])) != -1 and \
                    str(client_node.getpeername()).find(str(client_tupe[1])) != -1:
                client_node.send(sendMsg.encode(encoding="utf-8"))

    def __run_thread(self):
        while True:
            try:
                # 等待客户端连接
                client_socket, ip_port = self.tcp_socket.accept()
            except ConnectionAbortedError:
                break
            else:
                self.__clientList.append(client_socket)
                print("====== client_socket :" + str(client_socket.getpeername()))
                print("[新客户端]:", ip_port, "已连接")
                self.clientInfo_signal.emit(str(ip_port))
                client_socket.setblocking(False)    # 将套接字设置为非堵塞　
                # 有客户端连接后，创建一个线程将客户端套接字，IP端口传入recv函数，
                t1 = threading.Thread(target=self.__client_thread, args=(client_socket, ip_port, self.recvmsg_signal))
                # 启动线程
                t1.start()

    # 接收消息
    def __client_thread(self, client_socket, ip_port, recvmsg_signal):
        while True:
            if self.__disconnect_flag:
                break
            try:
                #该接收方式应该为阻塞接收方式
                recvMsg = client_socket.recv(2048)
                # 如果接收的消息长度不为0，则将其解码输出
            except: #TODO:这里应该需要抓取客户端断开连接的异常
                pass
            else:
                if recvMsg:
                    print("[客户端消息]", ip_port, ":", recvMsg.decode("utf-8"))
                    if self.recv_format == "Ascii":
                        recvmsg_signal.emit("[客户端消息]" + str(ip_port) + ": " + recvMsg.decode("utf-8"))
                    else:
                        recvMsgStr = ascii_to_hex(recvMsg.decode("utf-8"))
                        recvmsg_signal.emit("[客户端消息]" + str(ip_port) + ": " + str(recvMsgStr))
                else:
                    print("客户端", ip_port, "已下线")
                    client_socket.close()

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
        self.__clientList = []
        t1 = threading.Thread(target=self.__run_thread, args=())
        # 启动线程
        t1.start()

    def close(self):
        self.__disconnect_flag = True
        for client in self.__clientList:
            client.close()
        self.tcp_socket.close()

if __name__ == "__main__":
    tcp_sever = TcpSever()
    tcp_sever.create("192.168.100.102", 5000)
    tcp_sever.run()