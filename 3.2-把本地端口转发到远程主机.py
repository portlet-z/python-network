import asyncore
import socket


LOCAL_SERVER_HOST = "localhost"
REMOTE_SERVER_HOST = "www.google.com"
BUFSIZE = 4096


class PortForwarder(asyncore.dispatcher):
    def __init__(self, ip, port, remote_ip, remote_port, backlog=5):
        asyncore.dispatcher.__init__(self)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(backlog)

    def handle_accept(self):
        conn, addr = self.accept()
        print(f"Connected to: {addr}")
        Sender(Receiver(conn), self.remote_ip, self.remote_port)


class Receiver(asyncore.dispatcher):
    def __init__(self, conn):
        asyncore.dispatcher.__init__(self, conn)
        self.from_remote_buffer = b""
        self.to_remote_buffer = b""
        self.sender = None

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(BUFSIZE)
        self.from_remote_buffer += read

    def writable(self):
        return len(self.to_remote_buffer) > 0

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()


class Sender(asyncore.dispatcher):
    def __init__(self, receiver, remote_addr, remote_port):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver
        receiver.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remote_addr, remote_port))

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(BUFSIZE)
        self.receiver.to_remote_buffer += read

    def writeable(self):
        return len(self.receiver.from_remote_buffer) > 0

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()


if __name__ == '__main__':
    PortForwarder(LOCAL_SERVER_HOST, 8800, REMOTE_SERVER_HOST, 80)
    asyncore.loop()
