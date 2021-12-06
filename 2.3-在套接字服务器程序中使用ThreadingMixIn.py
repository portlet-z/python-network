import os
import socket
import threading
import socketserver

SERVER_HOST = "localhost"
SERVER_PORT = 0
BUF_SIZE = 1024


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(message)
        response = sock.recv(BUF_SIZE)
        print(f"Client received: {response}")


class ThreadTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        cur_thread = threading.current_thread()
        response = f"{cur_thread}, {data}".encode("utf8")
        self.request.sendall(response)


class ThreadTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    server = ThreadTCPServer(
        (SERVER_HOST, SERVER_PORT), ThreadTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f"Server loop running on thread: {server_thread.name}")
    client(ip, port, b"Hello from client 1")
    client(ip, port, b"Hello from client 2")
    client(ip, port, b"Hello from client 3")
    server.shutdown()
