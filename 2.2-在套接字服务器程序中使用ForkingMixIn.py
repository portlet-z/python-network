import os
import socket
import threading
import socketserver

SERVER_HOST = "localhost"
SERVER_PORT = 0  # 0表示动态分配端口号
BUF_SIZE = 1024
ECHO_MSG = "Hello echo server!"


class ForkingClient:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print(f"PID {current_process_id} Sending echo message to the server: {ECHO_MSG}")
        sent_data_length = self.sock.send(ECHO_MSG)
        print(f"Sent: {sent_data_length} characters, so far.")
        response = self.sock.recv(BUF_SIZE)
        print(f"PID {current_process_id} received: {response}")

    def shutdown(self):
        self.sock.close()


class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = f"{current_process_id}, {data}"
        print(f"Server sending response [current_process_id: data] = {response}")
        self.request.send(response)
        return


# The ForkingMixIn class is not available on Windows because there is no fork() on Windows.
class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever())
    server_thread.setDaemon(True)
    server_thread.start()
    print(f"Server loop running PID: {os.getpid()}")
    client1 = ForkingClient(ip, port)
    client1.run()
    client2 = ForkingClient(ip, port)
    client2.run()
    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()


if __name__ == '__main__':
    main()

