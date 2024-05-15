import numpy as np
import matplotlib as plt
from PIL import Image, ImageDraw, ImageColor
import time
import tkinter as tk
from tkinter import Canvas
import threading
from model.agent import Agent


def tick_agents():
    global agents
    for agent in agents:
        agent.tick()
    render_map()
    threading.Timer(1, tick_agents).start()


def render_map():
    global agents, canvas
    canvas.delete("all")
    for agent in agents:
        canvas.create_oval(agent.x - 10, agent.y - 10, agent.x + 10, agent.y + 10)
        canvas.create_line(agent.x, agent.y, agent.x + agent.direction[0]*20, agent.y + agent.direction[1]*20)


agents = [Agent(50, 50, (0, 10)), Agent(250, 50, (0, 10)), Agent(500, 50, (0, 10))]
root = tk.Tk()
root.geometry("1000x1000")
canvas = Canvas(root, width=1000, height=1000)
canvas.pack()

tick_agents()

root.mainloop()
