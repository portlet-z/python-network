import sys
import socket
import argparse


def main():
    # setup argument parsing
    parser = argparse.ArgumentParser(description="Socket Error Examples")
    parser.add_argument("--host", action="store", dest="host", required=True)
    parser.add_argument("--port", action="store", dest="port", type=int, required=True)
    parser.add_argument("--file", action="store", dest="file", required=False)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    filename = given_args.file
    print(given_args)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Error creating socket: {e}")
        sys.exit(1)

    try:
        s.connect((host, port))
    except socket.gaierror as e:
        print(f"Address-related error connection to server: {e}")
        sys.exit(1)
    except socket.error as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    try:
        s.sendall(f"GET {filename} HTTP/1.1\r\n".encode(encoding="utf-8"))
    except socket.error as e:
        print(f"Error sending data: {e}")
        sys.exit(1)

    while 1:
        try:
            buf = s.recv(2048)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            sys.exit(1)
        if not len(buf):
            break
        # write the received data
        sys.stdout.write(buf.decode('utf-8'))


if __name__ == '__main__':
    main()
