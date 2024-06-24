import math
from typing import List
from typing import Tuple

import numpy as np

from model.agent import Agent
from model.predator import Predator, affecting_predators
from model.task import Task, affecting_task
from util import normalize_vec, add_vec


class CouzinAgent(Agent):
    def __init__(self, x, y, direction: Tuple[float, float], speed, r_zone, o_zone, a_zone):
        super().__init__(x, y, direction, speed)
        self.r_zone = r_zone  # repulsion zone radius
        self.o_zone = o_zone  # orientation zone radius
        self.a_zone = a_zone  # attraction zone radius
        self.f_r = (0, 0)  # repulsion force
        self.f_o = (0, 0)  # orientation force
        self.f_a = (0, 0)  # attraction force

    def tick(self, agents, predators, tasks):
        """
        perform a simulation step

        1. search for agents within each zones
        2. calculate forces on the agent exerted by all other agents, predators and tasks
        3. adapt direction
        4. update position based on direction

        :param agents: list of agents in the simulation
        :param predators: list of predators in the simulation
        :param tasks: list of tasks in the simulation
        """
        # filter out self
        agents = list(filter(lambda a: a is not self, agents))

        # search for agents in zones

        agents_r, agents_o, agents_a = agents_between_radi(agents, (self.x, self.y), [self.r_zone, self.o_zone, self.a_zone])

        # search for predators that influence the agent
        predators_r = affecting_predators(predators, (self.x, self.y))

        # search for tasks that influence the agent
        t = affecting_task(tasks, (self.x, self.y))
        if t is not None:
            pos = np.linalg.norm([t.x - self.x, t.y - self.y])
            if pos <= t.action_radius:
                t.decrease_scope()

        # calculate forces
        self.f_r = calculate_repulsion_force(self, agents_r, predators_r)
        self.f_o = calculate_orientation_force(self, agents_o)
        self.f_a = calculate_attraction_force(self, agents_a, [] if t is None else [t])

        # change direction according to acting forces
        self.direction = tuple(np.sum([self._direction, self.f_r, self.f_o, self.f_a], axis=0))

        super().tick(agents, predators, tasks)


def agents_between_radi(agents, coords, radii) -> List[List[Agent]]:
    """
    calculate all agents within the field between an inner radius and an outer radius

    :param agents: list of agents
    :param coords: coordinates of agent
    :param radii: list of radii to sort agents into
    :return: list of lists of all agents at the different distances
    """
    agents_in_radius = [[] for _ in range(len(radii))]
    squared_distances = []
    for n in range(len(radii)):
        squared_distances.append(radii[n] * radii[n])
    for agent in agents:
        n = 0
        for min_dist in squared_distances:
            if math.pow(agent.x-coords[0], 2) + math.pow(agent.y-coords[1], 2) <= min_dist:
                agents_in_radius[n].append(agent)
                break
            else:
                n += 1

    return agents_in_radius


def calculate_repulsion_force(center, agents: List[Agent], predators: List[Predator]) -> Tuple[float, float]:
    """
    calculate repulsion force imposed by neighbouring agents and predators

    :param center: position of agent
    :param agents: neighbouring agents
    :param predators: nearby predators
    :return:
    """
    force = (0, 0)

    # repulsion from nearby agents
    for a in agents:
        d = normalize_vec((a.x - center.x, a.y - center.y))
        force = add_vec(force, d)

    # repulsion form nearby predators
    for p in predators:
        d = normalize_vec((p.x - center.x, p.y - center.y))
        # multiply with scalar because predator repulsion is stronger
        force = add_vec(force, tuple(np.multiply(d, p.force_scale)))

    return -force[0], -force[1]


def calculate_orientation_force(center, agents: List[Agent]) -> Tuple[float, float]:
    force = (0, 0)

    for a in agents:
        force = add_vec(force, normalize_vec(a.direction))

    return force


def calculate_attraction_force(center, agents: List[Agent], tasks: List[Task]) -> Tuple[float, float]:
    force = (0, 0)

    for a in agents:
        # normalized distance between center and all agents
        d = normalize_vec((a.x - center.x, a.y - center.y))
        force = add_vec(force, d)

    # attraction form nearby predators
    for t in tasks:
        d = normalize_vec((t.x - center.x, t.y - center.y))
        # multiply with scaler because task attraction is stronger
        force = add_vec(force, tuple(np.multiply(d, t.force_scale)))

    return force
