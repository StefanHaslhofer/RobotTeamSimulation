from typing import Tuple
import numpy as np


def normalize_vec(vec: Tuple[int, int]):
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm


class CouzinAgent:
    def __init__(self, x, y, direction: Tuple[int, int], r_zone, o_zone, a_zone):
        self.x = x
        self.y = y
        self._direction = normalize_vec(direction)
        self.r_zone = r_zone  # repulsion zone radius
        self.o_zone = o_zone  # orientation zone radius
        self.a_zone = a_zone  # attraction zone radius
        self.f_r = 0  # repulsion force
        self.f_o = 0  # orientation force
        self.f_a = 0  # attraction force

    def tick(self, agents, predators):
        """
        perform a simulation step

        1. search for agents within each zones
        2. calculate forces on the agent exerted by all other agents and predators
        3. adapt direction
        4. update position based on direction

        :param agents: list of agents in the simulation
        :param predators: list of predators in the simulation
        """
        self.x += self._direction[0]
        self.y += self._direction[1]

    @property
    def direction(self) -> Tuple[int, int]:
        return self._direction

    @direction.setter
    def direction(self, vec: Tuple[int, int]):
        self._direction = normalize_vec(vec)
