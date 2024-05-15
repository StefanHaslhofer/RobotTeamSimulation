from typing import Tuple
import numpy as np


def normalize_vec(vec: Tuple[int, int]):
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm


class Agent:
    def __init__(self, x, y, direction: Tuple[int, int]):
        self.x = x
        self.y = y
        self.direction = normalize_vec(direction)

    def tick(self):
        self.x += self.direction[0]
        self.y += self.direction[1]

    @property
    def direction(self) -> Tuple[int, int]:
        return self.direction

    @direction.setter
    def direction(self, vec: Tuple[int, int]):
        self.direction = normalize_vec(vec)
