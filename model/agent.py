from typing import Tuple
import numpy as np


def normalize_vec(vec):
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
