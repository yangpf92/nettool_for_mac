import socket
import uuid

'''
在列表中检测是否存在重复的val值
'''
def check_dup_ipaddr(ipaddr_list, val):
    if val in ipaddr_list:
        return True
    else:
        return False

class device_info():
    def get_host_info(self):
        self.hostname = socket.gethostname()
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        #self.mac = ":".join([mac[e:e + 2] for e in range(0, 11, 2)]

    def get_interface_info(self):
        self.ipaddr_list = list()
        ipaddrs = socket.getaddrinfo(socket.gethostname(), None)
        for item in ipaddrs:
            if ':' not in item[4][0]:
                pass
                #TODO: 这里的ip地址可能有重复，需要进行判断
                if check_dup_ipaddr(self.ipaddr_list, item[4][0]) != True:
                    self.ipaddr_list.append(item[4][0])
    def show(self):
        print("host name " + self.hostname)
        for ipaddr in self.ipaddr_list:
            print(ipaddr)

if __name__ == "__main__":
    device_info = device_info()
    device_info.get_host_info()
    device_info.get_interface_info()
    device_info.show()


