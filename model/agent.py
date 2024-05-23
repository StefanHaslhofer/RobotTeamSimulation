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
        self.x += self._direction[0]
        self.y += self._direction[1]
        # cap positions at the edge of the map
        self.x = min(MAP_SIZE_X, max(0, self.x))
        self.y = min(MAP_SIZE_Y, max(0, self.y))

    @property
    def direction(self) -> Tuple:
        return self._direction

    @direction.setter
    def direction(self, vec: Tuple[float, float]):
        self._direction = normalize_vec(vec)
