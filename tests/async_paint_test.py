import asyncio
import socket
import matplotlib.pyplot as plt
import numpy as np


SIZE = 10
grid = np.zeros((SIZE, SIZE))
changed = False
FPS = 10


class ServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr):
        data = data.split(b"\r\r")[0]
        print(f"Received from {addr}: {data}")
        try:
            change_grid(data)
        except Exception as e:
            print(e)

        # print('Send %r to %s' % (message, addr))
        # self.transport.sendto(data, addr)

    def error_received(self, exc):
        print("Error received:", exc)

    def connection_lost(self, exc):  # Or ended
        print("Error received:", exc)


async def display_image():
    while True:
        await asyncio.sleep(1 / FPS)
        if not changed:
            continue

        # display
        plt.imshow(grid, cmap="gray", alpha=1)
        plt.axis("off")
        plt.colorbar()

        # redraw
        plt.draw()
        plt.pause(0.0001)
        plt.clf()  # Clear the current figure


def change_grid(request: bytes):
    x, y = (np.array(request.decode().split(", "), dtype=float) * SIZE).astype(int)
    grid[x, y] += 1
    global changed
    changed = True
    print(grid.sum())


async def main():
    internal_ip = socket.gethostbyname(socket.gethostname())
    print(f"{internal_ip=}")

    print("Starting UDP server")
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        ServerProtocol, local_addr=(internal_ip, 12345)
    )

    task = asyncio.create_task(display_image())
    loop.call_later(3600, lambda: task.cancel())  # Serve for 1 hour.

    try:
        await task
    except asyncio.CancelledError:
        print("Serving time is over!")
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
