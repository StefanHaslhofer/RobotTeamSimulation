from typing import Tuple

from util import normalize_vec
from constants import *


class Agent:
    def __init__(self, x, y, direction: Tuple[float, float]):
        self.x = x
        self.y = y
        self.direction = direction

    def tick(self, agents, predators):
        # change position along direction vector
        self.x += self.direction[0]
        self.y += self.direction[1]
        # reflect movement at the edge of the map
        if self.x < 0 or self.x > MAP_SIZE_X:
            self.direction = (self.direction[0] * -1, self.direction[1])
            self.x += self.direction[0]
        if self.y < 0 or self.y > MAP_SIZE_X:
            self.direction = (self.direction[0], self.direction[1] * -1)
            self.y += self.direction[1]
        # cap movement at edge of map
        # self.x = min(MAP_SIZE_X, max(0, self.x))
        # self.y = min(MAP_SIZE_Y, max(0, self.y))

    @property
    def direction(self) -> Tuple:
        return self._direction

    @direction.setter
    def direction(self, vec: Tuple[float, float]):
        self._direction = normalize_vec(vec)
