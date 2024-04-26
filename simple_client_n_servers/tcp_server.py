import socket

from simple_client_n_servers.constants import server_address, server_port


def create_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_address, server_port))
        server_socket.listen()
        print(f"UDP server at {server_address=} listening on port {server_port}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode('utf-8')}")


if __name__ == "__main__":
    create_tcp_server()
