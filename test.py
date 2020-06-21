import threading
class Myclass(threading.Thread):
    def __init__(self, func, args, name):
        self.target = name
        threading.Thread.__init__(self, target=func)
        self.name = name
        self.args = args

def hello():
    print("111111")

if __name__ == "__main__":
    t = Myclass(hello, (1,), "test")
    t.start()
