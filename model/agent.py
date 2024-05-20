from typing import Tuple

from util import normalize_vec


class Agent:
    def __init__(self, x, y, direction: Tuple[float, float]):
        self.x = x
        self.y = y
        self.direction = direction

    def tick(self, agents, predators):
        # change position along direction vector
        self.x += self._direction[0]
        self.y += self._direction[1]

    @property
    def direction(self) -> Tuple:
        return self._direction

    @direction.setter
    def direction(self, vec: Tuple[float, float]):
        self._direction = normalize_vec(vec)
