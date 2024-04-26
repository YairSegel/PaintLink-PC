import socket

from simple_client_n_servers.constants import server_address, server_port


def create_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((server_address, server_port))
        print(f"UDP server at {server_address=} listening on port {server_port}...")
        while True:
            data, addr = server_socket.recvfrom(1024)
            if not data:
                break
            print(f"Received from {addr}: {data}")


if __name__ == "__main__":
    create_udp_server()
