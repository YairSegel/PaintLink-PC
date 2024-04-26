import socket

from simple_client_n_servers.constants import server_address, server_port


def send_messages_to_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_address, server_port))
        print("Connected")
        while True:
            data = input("next:\n")
            client_socket.sendall(data.encode("utf-8"))
            if not data:
                break


if __name__ == "__main__":
    send_messages_to_tcp_server()
