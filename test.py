# Author : Kelvin
# Date : 2019/2/3 21:51
import socketserver
from socket import *

ip_conf = ("192.168.100.102", 8880)
buffer_capcity = 1024


class Mysocket(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.request)
        print(self.client_address)

        while True:
            try:
                data = self.request.recv(buffer_capcity).decode("utf8")
                if len(data) <= 0:
                    self.request.close()
                    break
                else:
                    print("服务器收到信息：%s" % data)
                    self.request.send("服务器收到信息！".encode("utf8"))
            except Exception:
                print("==== close")
                self.request.close()
                break


if __name__ == "__main__":
    s = socketserver.ThreadingTCPServer(ip_conf, Mysocket)
    s.allow_reuse_address = True    #设置端口可重用
    s.serve_forever()