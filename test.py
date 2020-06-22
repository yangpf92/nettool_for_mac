my_str="192.168.50.3:39548"
my_tuple=tuple(my_str.split(":"))
print(my_tuple[0][2:-1])
print(my_tuple[1][1:-1])