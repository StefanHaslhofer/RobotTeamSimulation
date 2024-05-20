from typing import List
import numpy as np

from model.agent import Agent


class Predator(Agent):
    def __init__(self, x, y, radius, force_scale):
        super().__init__(x, y, (0, 0))
        self.x = x
        self.y = y
        self.radius = radius  # radius of area around predator that is effected by its repulsion force
        self.force_scale = force_scale


def affecting_predators(predators: List[Predator], coords) -> List[Predator]:
    af_pred = []
    for p in predators:
        pos = np.linalg.norm([p.x - coords[0], p.y - coords[1]])
        if pos <= p.radius:
            af_pred.append(p)

    return af_pred
