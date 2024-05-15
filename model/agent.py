from typing import Tuple


class Agent:
    def __init__(self, x, y, direction: Tuple[int, int]):
        self.x = x
        self.y = y
        self.direction = direction

    def tick(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
