import asyncio
import socket


class PrintServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr):
        print(f"Received from {addr}: {data}")

        # print('Send %r to %s' % (message, addr))
        self.transport.sendto(b"Freddie nice to meet\r\r", addr)

    def error_received(self, exc):
        print("Error received:", exc)

    def connection_lost(self, exc):  # Or ended
        print("Error received:", exc)


async def main():
    internal_ip = socket.gethostbyname(socket.gethostname())
    print(f"{internal_ip=}")

    print("Starting UDP server")
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        PrintServerProtocol, local_addr=(internal_ip, 12345)
    )

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    except asyncio.CancelledError:
        print("Serving time is over!")
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
