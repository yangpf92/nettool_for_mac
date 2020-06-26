def hex_to_ascii(hexList):
    asciiStr = ""
    for val in hexList:
        print(val)
        asciiStr += chr(int(val, 16))
    return asciiStr

def ascii_to_hex(asciiStr):
    hexStr = ""
    for val in asciiStr:
        hexStr += hex(ord(val)) + " "
    hexStr = hexStr[0:-1]   #去掉最后的空格
    return hexStr