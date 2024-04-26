import asyncio
import socket

from screen_handeler import Screen
from server_protocol import protocol_factory
from util import Flag


async def main():
    clients = {}
    ongoing_strokes = {}
    finished_strokes = []
    changed = Flag()

    internal_ip = socket.gethostbyname(socket.gethostname())
    internal_ip = "10.0.0.9"
    print(f"{internal_ip=}")

    print("Starting UDP server")
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        protocol_factory(clients, ongoing_strokes, finished_strokes, changed), local_addr=(internal_ip, 12345))

    screen = Screen(clients, ongoing_strokes, finished_strokes, changed)
    task = screen.get_program()
    loop.call_later(3600, lambda: task.cancel())  # Serve for 1 hour.

    try:
        await task
    except asyncio.CancelledError:
        print("Serving time is over!")
    finally:
        transport.close()
        screen.stop()


if __name__ == '__main__':
    asyncio.run(main())
