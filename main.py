import numpy as np
import matplotlib as plt
from PIL import Image, ImageDraw, ImageColor
import time
import tkinter as tk
from tkinter import Canvas
import threading
from model.couzin_agent import CouzinAgent
from model.predator import Predator
from constants import *


def tick_agents():
    global agents
    for agent in agents:
        agent.tick(agents, predators)
    render_map()
    threading.Timer(1.0 / 20, tick_agents).start()


def render_map():
    # TODO if agents leaves canvas he reenter canvas on opposite site
    global agents, predators, canvas
    canvas.delete("all")
    for agent in agents:
        canvas.create_oval(agent.x - AGENT_SIZE, agent.y - AGENT_SIZE, agent.x + AGENT_SIZE, agent.y + AGENT_SIZE,
                           fill='blue4')
        canvas.create_line(agent.x, agent.y, agent.x + int(agent.direction[0] * 20),
                           agent.y + int(agent.direction[1] * 20))

    for p in predators:
        canvas.create_oval(p.x - PREDATOR_SIZE, p.y - PREDATOR_SIZE, p.x + PREDATOR_SIZE, p.y + PREDATOR_SIZE,
                           fill='red2')


def motion(event):
    predators[0].x = canvas.canvasx(event.x)
    predators[0].y = canvas.canvasy(event.y)


agents = []
agents.append(CouzinAgent(50, 50, (0, 10), 20, 50, 300))
agents.append(CouzinAgent(250, 50, (0, 10), 20, 50, 300))
agents.append(CouzinAgent(600, 50, (0, 10), 20, 50, 300))
agents.append(CouzinAgent(850, 50, (0, 10), 20, 50, 300))
agents.append(CouzinAgent(600, 150, (0, 10), 20, 50, 300))

predators = []
predators.append(Predator(500, 500, 100, 5))

root = tk.Tk()
root.geometry(f'{MAP_SIZE_X}x{MAP_SIZE_Y}')
canvas = Canvas(root, width=MAP_SIZE_X, height=MAP_SIZE_Y)
canvas.configure(bg='SkyBlue1')
canvas.bind("<Motion>", motion)
canvas.pack()

tick_agents()

root.mainloop()
