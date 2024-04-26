from dataclasses import dataclass
from struct import unpack
from typing import Callable

from util import *


@dataclass
class ServerProtocol:
    clients: dict[ClientAddress, ColorPoint]
    ongoing_strokes: dict[ClientAddress, Stroke]
    finished_strokes: list[Stroke]
    change_flag: Flag

    def connection_made(self, transport):
        self.transport = transport  # noqa: used for returning messages

    def datagram_received(self, data: bytes, addr: ClientAddress):
        if b"Where are you?" in data:  # check if packet is dhcp packet
            print(f"Replying to DHCP discover packet from {addr}")
            self.transport.sendto(b"Freddie nice to meet\r\r", addr)  # add useful info
            return
        elif len(data) != 16:
            return

        # todo: do encryption
        # todo: try to add stabilizer

        old_position = self.clients.get(addr)
        current_position: ColorPoint = unpack(">ffi", data[:12])  # noqa
        if old_position is None:  # New client
            print(f"New client: {addr}")
            self.clients[addr] = current_position
            self.ongoing_strokes[addr] = Stroke()
        else:
            self.clients[addr] = nudge_point(old_position, current_position)

        pressed = unpack(">i", data[12:])[0]
        if pressed:
            self.ongoing_strokes[addr].append(self.clients[addr][:2])
        else:
            current_stroke = self.ongoing_strokes[addr]
            if current_stroke.points:
                current_stroke.color = current_position[2]
                self.finished_strokes.append(current_stroke)
                self.ongoing_strokes[addr] = Stroke()

        self.change_flag.triggered = True

    @staticmethod
    def error_received(exc):
        print("Error received: ", exc)

    @staticmethod
    def connection_lost(exc):  # Or ended
        print("Error received: ", exc)


def protocol_factory(clients: dict[ClientAddress, ColorPoint], ongoing_strokes: dict[ClientAddress, Stroke],
                     finished_strokes: list[Stroke], change_flag: Flag) -> Callable:
    return lambda: ServerProtocol(clients, ongoing_strokes, finished_strokes, change_flag)


def nudge_point(p1: ColorPoint, p2: ColorPoint) -> ColorPoint:
    amp = 10  # when rps = 100
    return (p1[0] * (amp - 1) + p2[0]) / amp, (p1[1] * (amp - 1) + p2[1]) / amp, p2[2]
