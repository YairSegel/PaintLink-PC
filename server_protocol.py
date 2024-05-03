from dataclasses import dataclass, field
from struct import unpack
from typing import Callable

from signatures import Verifier
from util import *


@dataclass
class ServerProtocol:
    clients: dict[ClientAddress, ColorPoint]
    ongoing_strokes: dict[ClientAddress, Stroke]
    finished_strokes: list[Stroke]
    change_flag: Flag

    verifiers: dict[ClientAddress, Verifier] = field(default_factory=dict)

    def connection_made(self, transport):
        self.transport = transport  # noqa: used for returning messages

    def datagram_received(self, data: bytes, full_addr: ClientAddress):
        print(data)
        addr = full_addr[0]

        if len(data) != 500:  # check if packet is dhcp packet
            try:
                self.verifiers[addr] = Verifier(data.strip())
                print(f"Replying to DHCP discover packet from {addr}")
                self.transport.sendto(b"Freddie nice to meet\r\r", full_addr)  # add useful info
            finally:
                return

        if not self.verifiers.get(addr):
            return

        # todo: do encryption
        # todo: try to add stabilizer
        if not self.verifiers[addr].verify(data[:16], data[20:20+unpack(">i", data[16:20])[0]]):  # todo: clean this
            print(f"Got a non-valid request from {addr}")
            return
        print("bonanza")

        old_position = self.clients.get(addr)
        current_position: ColorPoint = unpack(">ffi", data[:12])  # noqa
        if old_position is None:  # New client todo: move up
            print(f"New client: {addr}")
            self.clients[addr] = current_position
            self.ongoing_strokes[addr] = Stroke()
        else:
            self.clients[addr] = nudge_point(old_position, current_position)

        pressed = unpack(">i", data[12:16])[0]
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
