import numpy as np
import matplotlib as plt
from PIL import Image, ImageDraw, ImageColor
import time
import tkinter as tk
from tkinter import Canvas
import threading
from model.couzin_agent import CouzinAgent

AGENT_SIZE = 5
PREDATOR_SIZE = 10


def tick_agents():
    global agents
    for agent in agents:
        agent.tick(agents, {})
    render_map()
    threading.Timer(1.0 / 20, tick_agents).start()


def render_map():
    # TODO if agents leaves canvas he reenter canvas on opposite site
    global agents, canvas
    canvas.delete("all")
    for agent in agents:
        canvas.create_oval(agent.x - AGENT_SIZE, agent.y - AGENT_SIZE, agent.x + AGENT_SIZE, agent.y + AGENT_SIZE,
                           fill='blue4')
        canvas.create_line(agent.x, agent.y, agent.x + int(agent.direction[0] * 20),
                           agent.y + int(agent.direction[1] * 20))
    canvas.create_oval(predatorPos[0] - PREDATOR_SIZE, predatorPos[1] - PREDATOR_SIZE, predatorPos[0] + PREDATOR_SIZE,
                       predatorPos[1] + PREDATOR_SIZE, fill='red2')


def motion(event):
    global predatorPos
    predatorPos = (canvas.canvasx(event.x), canvas.canvasy(event.y))


agents = []
agents.append(CouzinAgent(50, 50, (0, 10), 20, 50, 300))
agents.append(CouzinAgent(250, 50, (0, 10), 20, 50, 300))
agents.append(CouzinAgent(600, 50, (0, 10), 20, 50, 300))
agents.append(CouzinAgent(850, 50, (0, 10), 20, 50, 300))
agents.append(CouzinAgent(600, 150, (0, 10), 20, 50, 300))
predatorPos = (500, 500)
root = tk.Tk()
root.geometry("1000x1000")
canvas = Canvas(root, width=1000, height=1000)
canvas.configure(bg='SkyBlue1')
canvas.bind("<Motion>", motion)
canvas.pack()

tick_agents()

root.mainloop()
