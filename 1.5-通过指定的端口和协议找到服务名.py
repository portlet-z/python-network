import socket


def find_service_name():
    protocol_name = 'tcp'
    for port in [80, 25]:
        print(f"Port: {port} => service name: {socket.getservbyport(port, protocol_name)}")
    print(f"Port: 53 => service name: {socket.getservbyport(53, 'udp')}")


if __name__ == '__main__':
    find_service_name()
