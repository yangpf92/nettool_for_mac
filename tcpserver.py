# Author : Kelvin
# Date : 2019/2/3 21:51
import socketserver
import threading
import time
import sys

buffer_capcity = 1024
global g_nettoolwindow

class Mysocket(socketserver.BaseRequestHandler):
    global g_nettoolwindow
    def __sockRecv_thread_cb(self):
        while True:
            recv_msg = self.request.recv(buffer_capcity).decode("utf8")
            if len(recv_msg) < 0:
                self.request.close()
                break
            else:
                g_nettoolwindow.textBrowserNetRecv.insertPlainText(recv_msg)


    def __sockSend_thread_cb(self):
        while True:
            if len(g_nettoolwindow.send_msg) > 0:
                self.request.send(g_nettoolwindow.send_msg.encode("utf8"))
                g_nettoolwindow.send_msg = ""

    def handle(self):
        print(self.request)
        print(self.client_address)
        #创建两个线程
        self.sock_recv_t = threading.Thread(target=self.__sockRecv_thread_cb, args=())
        self.sock_recv_t.setDaemon(True)    #设置后台，主线程退出则创建的子线程退出
        self.sock_recv_t.start()
        self.sock_send_t = threading.Thread(target=self.__sockSend_thread_cb, args=())
        self.sock_send_t.setDaemon(True)  # 设置后台，主线程退出则创建的子线程退出
        self.sock_send_t.start()
        while True:
            time.sleep(3)

    def finish(self):
        self.request.close()  # 关闭套接字

class TcpSever():
    def create(self, nettoolwindow, server_addr, port):
        global g_nettoolwindow
        g_nettoolwindow = nettoolwindow
        self.server_addr = server_addr
        self.port = port
        self.sock = socketserver.ThreadingTCPServer((self.server_addr, self.port), Mysocket)
        self.sock.allow_reuse_address = True  # 设置端口可重用

    def run(self):
        self.sock.serve_forever()




if __name__ == "__main__":
    tcp_sever = TcpSever()
    tcp_sever.create("192.168.100.102", 5000)
    tcp_sever.run()