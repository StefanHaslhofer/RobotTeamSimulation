import random
import threading
import tkinter as tk
from tkinter import Canvas

import model.predator
from constants import *
from model.couzin_agent import CouzinAgent
from model.predator import Predator
from model.task import Task


def tick_agents():
    global agents, tasks, predators
    # remove tasks with scope 0
    tasks[:] = filter(lambda t: t.scope > 0, tasks)
    for agent in agents:
        agent.tick(agents, predators, tasks)
    for pred in predators:
        pred.tick(agents, predators, tasks)
    render_map()
    threading.Timer(1.0 / 20, tick_agents).start()


def render_map():
    # TODO if agents leaves canvas he reenter canvas on opposite site
    global agents, predators, tasks, canvas
    canvas.delete("all")
    for agent in agents:
        canvas.create_oval(agent.x - AGENT_SIZE, agent.y - AGENT_SIZE, agent.x + AGENT_SIZE, agent.y + AGENT_SIZE,
                           fill='blue4')
        canvas.create_line(agent.x, agent.y, agent.x + int(agent.direction[0] * 20),
                           agent.y + int(agent.direction[1] * 20))

    for p in predators:
        canvas.create_oval(p.x - PREDATOR_SIZE, p.y - PREDATOR_SIZE, p.x + PREDATOR_SIZE, p.y + PREDATOR_SIZE,
                           fill='red2')

    for t in tasks:
        size = TASK_SIZE * (t.scope / TASK_SCOPE)
        # size of task is equal to its scope
        canvas.create_oval(t.x - size, t.y - size, t.x + size, t.y + size, fill='green2')


def motion(event):
    model.predator.target_x = canvas.canvasx(event.x)
    model.predator.target_y = canvas.canvasy(event.y)


agents = []
for i in range(20):
    agents.append(
        CouzinAgent(
            random.randrange(0, MAP_SIZE_X),
            random.randrange(0, MAP_SIZE_Y),
            (random.randrange(-1, 1), random.randrange(-1, 1)),
            3,
            20,
            50,
            300
        )
    )

tasks = []
for i in range(20):
    tasks.append(
        Task(
            random.randrange(0, MAP_SIZE_X),
            random.randrange(0, MAP_SIZE_Y),
            TASK_SCOPE,
            TASK_ATTRACTION_RADIUS,
            TASK_FORCE_SCALE
        )
    )

predators = [Predator(500, 500, 8, 100, 5)]

root = tk.Tk()
root.geometry(f'{MAP_SIZE_X}x{MAP_SIZE_Y}')
canvas = Canvas(root, width=MAP_SIZE_X, height=MAP_SIZE_Y)
canvas.configure(bg='SkyBlue1')
canvas.bind("<Motion>", motion)
canvas.pack()

tick_agents()

root.mainloop()
