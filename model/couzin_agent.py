from typing import Tuple
from typing import List
import numpy as np

from model.agent import Agent
from util import normalize_vec, add_vec


class CouzinAgent(Agent):
    def __init__(self, x, y, direction: Tuple[float, float], r_zone, o_zone, a_zone):
        super().__init__(x, y, direction)
        self.r_zone = r_zone  # repulsion zone radius
        self.o_zone = o_zone  # orientation zone radius
        self.a_zone = a_zone  # attraction zone radius
        self.f_r = (0, 0)  # repulsion force
        self.f_o = (0, 0)  # orientation force
        self.f_a = (0, 0)  # attraction force

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
        # filter out self
        agents = list(filter(lambda a: a is not self, agents))

        # search for agents in zones
        agents_r = agents_between_radi(agents, (self.x, self.y), 0, self.r_zone)
        agents_o = agents_between_radi(agents, (self.x, self.y), self.r_zone, self.o_zone)
        agents_a = agents_between_radi(agents, (self.x, self.y), self.o_zone, self.a_zone)

        # calculate forces
        self.f_r = calculate_repulsion_force(self, agents_r)
        self.f_o = calculate_orientation_force(self, agents_o)
        self.f_a = calculate_attraction_force(self, agents_a)

        # change direction according to acting forces
        self.direction = tuple(np.sum([self._direction, self.f_r, self.f_o, self.f_a], axis=0))

        super().tick(agents, predators)


def agents_between_radi(agents, center, inner, outer) -> List[CouzinAgent]:
    """
    calculate all agents within the field between an inner radius and an outer radius

    :param agents: list of agents
    :param inner: inner radius around agent
    :param outer: outer radius around agent
    :return: list of all agents within radius
    """
    agents_in_radius = []
    for agent in agents:
        pos = np.linalg.norm([agent.x - center[0], agent.y - center[1]])
        if inner < pos <= outer:
            agents_in_radius.append(agent)

    return agents_in_radius


def calculate_repulsion_force(center, agents: List[CouzinAgent]) -> Tuple[float, float]:
    force = (0, 0)

    for a in agents:
        d = normalize_vec((a.x - center.x, a.y - center.y))
        force = add_vec(force, d)

    return -force[0], -force[1]


def calculate_orientation_force(center, agents: List[CouzinAgent]) -> Tuple[float, float]:
    force = (0, 0)

    for a in agents:
        force = add_vec(force, normalize_vec(a.direction))

    return force


def calculate_attraction_force(center, agents: List[CouzinAgent]) -> Tuple[float, float]:
    force = (0, 0)

    for a in agents:
        # normalized distance between center and all agents
        d = normalize_vec((a.x - center.x, a.y - center.y))
        force = add_vec(force, d)

    return force
