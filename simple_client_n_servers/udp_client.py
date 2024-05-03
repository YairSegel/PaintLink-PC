import socket

from simple_client_n_servers.constants import server_address, server_port


def send_messages_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            data = input("next:\n")
            client_socket.sendto(data.encode("utf-8"), ("255.255.255.255", server_port))
            if not data:
                break
            print(client_socket.recv(1024))


if __name__ == "__main__":
    send_messages_to_server()
