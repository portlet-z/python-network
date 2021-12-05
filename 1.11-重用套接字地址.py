import socket
import sys


def reuse_socket_addr():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    old_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print(f"Old sock state: {old_state}")
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print(f"New sock state: {new_state}")
    local_port = 8282
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('', local_port))
    srv.listen(1)
    print(f"Listening on port: {local_port}")
    while True:
        try:
            connection, addr = srv.accept()
            print(f"Connected by {addr[0]} : {addr[1]}")
        except KeyboardInterrupt:
            break
        except socket.error as msg:
            print(msg)


if __name__ == '__main__':
    reuse_socket_addr()
