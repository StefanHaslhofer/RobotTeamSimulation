from typing import List

import numpy as np

from model.agent import Agent


class Task(Agent):
    def __init__(self, x, y, scope, radius, force_scale):
        super().__init__(x, y, (0, 0), 0)
        self.scope = scope
        self.radius = radius  # radius of attraction area around task
        self.force_scale = force_scale

    def decrease_scope(self):
        if self.scope > 0:
            self.scope -= 1


def affecting_tasks(tasks: List[Task], coords) -> List[Task]:
    af_tasks = []
    for t in tasks:
        pos = np.linalg.norm([t.x - coords[0], t.y - coords[1]])
        if pos <= t.radius:
            af_tasks.append(t)

    return af_tasks
