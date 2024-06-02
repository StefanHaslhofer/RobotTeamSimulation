from typing import List

import numpy as np

from constants import *
from model.agent import Agent
from util import normalize_vec

target_x = MAP_SIZE_X
target_y = MAP_SIZE_Y


class Predator(Agent):
    def __init__(self, x, y, speed, radius, force_scale):
        super().__init__(x, y, (0, 0), speed)
        self.x = x
        self.y = y
        self.radius = radius  # radius of area around predator that is effected by its repulsion force
        self.force_scale = force_scale

    def tick(self, agents, predators, tasks):
        global target_x, target_y
        self.direction = normalize_vec((target_x - self.x, target_y - self.y))
        super().tick(agents, predators, tasks)


def affecting_predators(predators: List[Predator], coords) -> List[Predator]:
    af_pred = []
    for p in predators:
        pos = np.linalg.norm([p.x - coords[0], p.y - coords[1]])
        if pos <= p.radius:
            af_pred.append(p)

    return af_pred
