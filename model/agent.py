from typing import Tuple

from constants import *
from util import normalize_vec


class Agent:
    def __init__(self, x, y, direction: Tuple[float, float], speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed

    def tick(self, agents, predators, tasks):
        center = (MAP_SIZE_X/2 - self.x, MAP_SIZE_Y/2 - self.y)
        # reflect movement at the edge of the map to the center
        if self.x < MAP_INNER_BORDER or self.x > MAP_SIZE_X - MAP_INNER_BORDER:
            self.direction = center
        if self.y < MAP_INNER_BORDER or self.y > MAP_SIZE_Y - MAP_INNER_BORDER:
            self.direction = center
        # change position along direction vector
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        # cap movement at edge of map
        # self.x = min(MAP_SIZE_X, max(0, self.x))
        # self.y = min(MAP_SIZE_Y, max(0, self.y))

    @property
    def direction(self) -> Tuple:
        return self._direction

    @direction.setter
    def direction(self, vec: Tuple[float, float]):
        self._direction = normalize_vec(vec)
