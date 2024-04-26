from typing import Any

import numpy as np
import pygame
from scipy.interpolate import splprep, splev

DEFAULT_SCREEN_SIZE = (800, 600)
CANVAS_RESOLUTION = (800, 600)
FPS = 60
POINTER_RADIUS = 40
POINT_RADIUS = 5

SKETCHBOOK = False
INDIVIDUAL_POINTS = False


def line_finder(points: dict[tuple[float, float], Any]):
    # https://stackoverflow.com/questions/31464345/fitting-a-closed-curve-to-a-set-of-points
    points = np.array(tuple(points.keys()))

    tck, u = splprep(points.T, s=0)  # noqa
    u_new = np.linspace(u.min(), u.max(), 1000)
    x_new, y_new = splev(u_new, tck, der=0)
    return tuple(zip(x_new, y_new))


pygame.init()
window = pygame.display.set_mode(
    DEFAULT_SCREEN_SIZE, pygame.RESIZABLE
)  # pygame.FULLSCREEN removes controls
clock = pygame.time.Clock()

current_line = None
current_line_points = {}  # needs to be ordered with no duplicates
static_points = set()
static_lines = set()

pressed = False
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not SKETCHBOOK:
        window.fill((0, 0, 0))
    for point in static_points:
        pygame.draw.circle(window, 0xFF0000, point, POINT_RADIUS)
    for line in static_lines:
        pygame.draw.lines(window, 0x00FF00, False, line, width=POINT_RADIUS - 1)
    if current_line:
        pygame.draw.lines(window, 0x00FF00, False, current_line, width=POINT_RADIUS - 1)

    if pygame.mouse.get_pressed(3)[0]:
        pressed = True
        current_line_points[pygame.mouse.get_pos()] = 0
        static_points.add(pygame.mouse.get_pos())

        if len(current_line_points) > 3:  # magic number, makes things not crash
            current_line = line_finder(current_line_points)

    elif pressed and not INDIVIDUAL_POINTS:
        if current_line:
            static_lines.add(current_line)
            current_line = None
        current_line_points = {}
        pressed = False

    pygame.display.flip()

pygame.quit()
