import socket


def get_remote_machine_info():
    remote_host = 'www.baidu.com'
    try:
        print(f"IP address: {socket.gethostbyname(remote_host)}")
    except socket.error as err:
        print(f"{remote_host}, {err}")


if __name__ == '__main__':
    get_remote_machine_info()
