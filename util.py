# Typing stuff
Point = tuple[float, float]
Color = int  # 0xFFFFFF
ColorPoint = tuple[float, float, Color]
ClientAddress = tuple[str, int] or str  # ("127.0.0.1", 12345)


class Stroke:  # Extending list makes init take too long
    def __init__(self, color: Color = 0x000000):
        self.points: list[Point] = []
        self.color = color

        self.append = self.points.append  # slower init for faster appending


class Flag:
    def __init__(self):
        self.triggered: bool = False

# class P:
#     def __init__(self, x, y, c):
#         self.x: float = x
#         self.y: float = y
#         self.color: int = c
#
#     def move_to(self, destination, amp: int = 10):
#         self.x = (self.x * (amp - 1) + destination.x) / amp
#         self.y = (self.y * (amp - 1) + destination.y) / amp
#         self.color = destination.color
#
#     def __add__(self, other):
#         amp: int = 10
#         return P((self.x * (amp - 1) + other.x) / amp, (self.y * (amp - 1) + other.y) / amp, other.color)
#
#     def as_tuple(self, scale: tuple[float, float] or float = 1):
#         if type(scale) == tuple or type(scale) == list:
#             return self.x * scale[0], self.y * scale[1]
#         return self.x * scale, self.y * scale
