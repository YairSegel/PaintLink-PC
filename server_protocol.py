from dataclasses import dataclass, field
from struct import unpack
from typing import Callable, Any

from signatures import Verifier
from util import *


@dataclass
class ServerProtocol:
    clients: dict[IP, ColorPoint]
    ongoing_strokes: dict[IP, Stroke]
    finished_strokes: list[Stroke]
    change_flag: Flag

    _verifiers: dict[IP, Verifier] = field(default_factory=dict)
    _transport: Any = None  # used for returning messages

    def connection_made(self, transport) -> None:
        self._transport = transport

    def datagram_received(self, data: bytes, full_address: ClientAddress) -> None:
        client_ip = full_address[0]

        # Ping requests
        if len(data) != 500:
            try:
                self._verifiers[client_ip] = Verifier(data.strip())
                self.ongoing_strokes[client_ip] = Stroke()
                print(f"Replying to ping packet from new client at: {client_ip}")
                self._transport.sendto(b"Freddie nice to meet\r\r", full_address)  # add useful info
            finally:
                return

        # Verify signature
        client_verifier: Verifier = self._verifiers.get(client_ip)
        *current_position, pressed, signature_length = unpack(">ff iii", data[:20])
        if (client_verifier is None) or (not client_verifier.verify(data[:16], data[20:20 + signature_length])):
            print(f"Got a non-valid request from {client_ip}")
            return

        # Update positions
        self.clients[client_ip] = nudge_point(self.clients.get(client_ip), current_position)
        if pressed:
            self.ongoing_strokes[client_ip].append(self.clients[client_ip][:2])
        else:
            current_stroke = self.ongoing_strokes[client_ip]
            if current_stroke.points:
                current_stroke.color = current_position[2]
                self.finished_strokes.append(current_stroke)
                self.ongoing_strokes[client_ip] = Stroke()

        self.change_flag.triggered = True

    @staticmethod
    def error_received(exc) -> None:
        print("Error received: ", exc)

    @staticmethod
    def connection_lost(exc) -> None:
        print("Error received: ", exc)


def protocol_factory(clients: dict[IP, ColorPoint], ongoing_strokes: dict[IP, Stroke],
                     finished_strokes: list[Stroke], change_flag: Flag) -> Callable[[], ServerProtocol]:
    return lambda: ServerProtocol(clients, ongoing_strokes, finished_strokes, change_flag)
