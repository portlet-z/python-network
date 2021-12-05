import socket


host = "localhost"
data_payload = 2048
backlog = 5


def echo_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (host, port)
    print(f"Starting up echo server on {server_address}")
    sock.bind(server_address)
    sock.listen(backlog)
    while True:
        print(f"Waiting to receive message from client")
        client, address = sock.accept()
        data = client.recv(data_payload)
        if data:
            print(f"Data: {data}")
            client.send(data)
            print(f"sent {data} bytes back to {address}")
            client.close()


def echo_client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    print(f"Connecting to {server_address}")
    sock.connect(server_address)
    try:
        message = b"Test message. This will be echoed"
        print(f"Sending {message}")
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print(f"Received: {data}")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Other exceptionL {e}")
    finally:
        print(f"Closing connection to the server")
        sock.close()


if __name__ == '__main__':
    #echo_server(8888)
    echo_client(8888)
