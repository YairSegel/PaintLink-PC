# Typing stuff
Point = tuple[float, float]
Color = int  # 0xFFFFFF
ColorPoint = tuple[float, float, Color]
IP = str
ClientAddress = tuple[IP, int]  # ("127.0.0.1", 12345)


class Stroke:  # extending list makes init take too long
    def __init__(self, color: Color = 0x000000):
        self.points: list[Point] = []
        self.color = color

        self.append = self.points.append  # slower init for faster appending


class Flag:
    def __init__(self):
        self.triggered: bool = False


def nudge_point(p1: ColorPoint, p2: ColorPoint) -> ColorPoint:  # todo: try to add stabilizer
    if p1 is None:
        return p2
    amp = 10  # when rps = 100
    return (p1[0] * (amp - 1) + p2[0]) / amp, (p1[1] * (amp - 1) + p2[1]) / amp, p2[2]
