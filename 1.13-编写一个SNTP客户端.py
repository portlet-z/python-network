import socket
import struct
import time


NTP_SERVER = ("0.cn.pool.ntp.org", 123)
TIME_1970 = 2208988800


def sntp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, NTP_SERVER)
    data, address = client.recvfrom(1024)
    if data:
        print(f"Response received from: {address}")
        print(data)
        t = struct.unpack('!12I', data)[10]
        t -= TIME_1970
        print(f"Time = {time.ctime(t)}")
        print(time.ctime(TIME_1970))


if __name__ == '__main__':
    sntp_client()
