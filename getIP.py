from os import popen
from re import findall, I

def getIPv6Address():
    output = popen("ipconfig /all").read()
    # print(output)
    result = findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, I)
    return result[0][0]