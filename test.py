#global Age
Age=10
class A():
    def __init__(self):
        global Age
        Age = 20
        print(Age)

a = A()
print(Age)