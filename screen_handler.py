import asyncio
from dataclasses import dataclass
from tkinter.filedialog import asksaveasfile

import pygame
from numpy import array as np_array, linspace as np_linspace
from scipy.interpolate import splev, splprep

from util import *

DEFAULT_SCREEN_SIZE = (800, 600)
CANVAS_RESOLUTION = (800, 600)
FPS = 60
POINTER_RADIUS = 40
POINT_RADIUS = 5


@dataclass
class Screen:
    clients: dict[IP, ColorPoint]
    ongoing_strokes: dict[IP, Stroke]
    finished_strokes: list[Stroke]
    update_flag: Flag

    def __post_init__(self):
        pygame.init()
        self.permanent_canvas = pygame.Surface(CANVAS_RESOLUTION)
        self.permanent_canvas.fill((255, 255, 255))

        self.pointer_svg = pygame.transform.scale(pygame.image.load("client.svg"),
                                                  (POINTER_RADIUS * 2, POINTER_RADIUS * 2))

    @staticmethod
    def stop() -> None:
        pygame.quit()

    def get_program(self) -> asyncio.Task:
        return asyncio.create_task(self._run())

    async def _run(self) -> None:
        window = pygame.display.set_mode(DEFAULT_SCREEN_SIZE, pygame.RESIZABLE)  # pygame.FULLSCREEN removes controls
        window_size = window.get_size()
        while True:
            # self.clock.tick(FPS)  # doesn't let the server run
            await asyncio.sleep(1 / FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        self.save_canvas()
                    finally:
                        return

            if not self.update_flag.triggered:
                continue
            else:  # Updating screen
                self.update_flag.triggered = False

            while self.finished_strokes:
                stroke = self.finished_strokes.pop()
                if len(stroke.points) <= 3:
                    continue  # TODO: fix this crash!
                pygame.draw.lines(self.permanent_canvas, stroke.color, False, line_finder(stroke.points),
                                  width=POINT_RADIUS - 1)
            window.blit(self.permanent_canvas, self.permanent_canvas.get_rect(center=window.get_rect().center))

            for stroke in self.ongoing_strokes.values():
                points = stroke.points
                if len(points) <= 3:
                    continue
                pygame.draw.lines(window, 0x000000, False, line_finder(points), width=POINT_RADIUS - 1)

            for client in self.clients.values():
                client_pos = (client[0] * window_size[0], client[1] * window_size[1])
                window.blit(self.pointer_svg, self.pointer_svg.get_rect(center=client_pos))
                pygame.draw.circle(window, client[2], client_pos, POINT_RADIUS)
            pygame.display.flip()

    def save_canvas(self):
        with asksaveasfile(initialfile='Untitled.png', defaultextension=".png") as f:
            print(f"Saving canvas at: {(path := f.name)}")
        pygame.image.save_extended(self.permanent_canvas, path)


def line_finder(points: list[Point]) -> tuple[Point, ...]:
    # make sure that points contains no consecutive duplicates!
    # https://stackoverflow.com/questions/31464345/fitting-a-closed-curve-to-a-set-of-points
    tck, u = splprep(np_array(points).T, s=0)  # noqa
    u_new = np_linspace(u.min(), u.max(), 1000)
    x_new, y_new = splev(u_new, tck, der=0)

    x_new *= CANVAS_RESOLUTION[0]
    y_new *= CANVAS_RESOLUTION[1]
    return tuple(zip(x_new, y_new))
