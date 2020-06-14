# Author : Kelvin
# Date : 2019/2/3 21:51
import socketserver
from main import *
import sys
import main

buffer_capcity = 1024

g_nettool_window=NetToolWindow()

class Mysocket(socketserver.BaseRequestHandler):

    def handle(self):
        print(self.request)
        print(self.client_address)

        while True:
            #try:
                data = self.request.recv(buffer_capcity).decode("utf8")
                if len(data) <= 0:
                    self.request.close()
                    break
                else:
                    #print("服务器收到信息：%s" % data)
                    g_nettool_window.textBrowserNetRecv.insertPlainText(data)
                    self.request.send("recv hello word！".encode("utf8"))
            #except Exception:
            #    print("==== close")
            #    self.request.close()
            #    break

class TcpSever():
    def create(self, nettool_window, server_addr, port):
        global g_nettool_window
        g_nettool_window = nettool_window
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