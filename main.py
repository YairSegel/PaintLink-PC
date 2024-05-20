import asyncio
import socket

from screen_handler import Screen
from server_protocol import protocol_factory
from util import Flag


async def main():
    clients = {}
    ongoing_strokes = {}
    finished_strokes = []
    changed = Flag()

    internal_ip = socket.gethostbyname(socket.gethostname())
    port = 12345
    lifetime = 3600  # in seconds
    # internal_ip = "10.0.0.9"

    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        protocol_factory(clients, ongoing_strokes, finished_strokes, changed), local_addr=(internal_ip, port))  # noqa
    print(f"Starting server at {internal_ip=} on {port=}")

    screen = Screen(clients, ongoing_strokes, finished_strokes, changed)
    task = screen.get_program()
    loop.call_later(lifetime, lambda: task.cancel())

    try:
        await task
    except asyncio.CancelledError:
        print("Serving time is over!")
    finally:
        transport.close()
        screen.stop()


if __name__ == '__main__':
    asyncio.run(main())
