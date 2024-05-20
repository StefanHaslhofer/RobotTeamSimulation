import numpy as np
import matplotlib as plt
from PIL import Image, ImageDraw, ImageColor
import time
import tkinter as tk
from tkinter import Canvas
import threading
from model.agent import CouzinAgent


def tick_agents():
    global agents
    for agent in agents:
        agent.tick(agents, {})
    render_map()
    threading.Timer(1.0/20, tick_agents).start()


def render_map():
    global agents, canvas
    canvas.delete("all")
    for agent in agents:
        canvas.create_oval(agent.x - 10, agent.y - 10, agent.x + 10, agent.y + 10, fill = 'blue4')
        canvas.create_line(agent.x, agent.y, agent.x + int(agent.direction[0]*20), agent.y + int(agent.direction[1]*20))
    canvas.create_oval(predatorPos[0] - 20, predatorPos[1] - 20, predatorPos[0] + 20, predatorPos[1] + 20, fill = 'red2')

def motion(event):
    global predatorPos
    predatorPos = (canvas.canvasx(event.x), canvas.canvasy(event.y))


agents = []
agents.append(CouzinAgent(50, 50, (0, 10), 10, 20, 10))
agents.append(CouzinAgent(250, 50, (0, 10), 10, 20, 10))
agents.append(CouzinAgent(600, 50, (0, 10), 10, 20, 10))
predatorPos = (500, 500)
root = tk.Tk()
root.geometry("1000x1000")
canvas = Canvas(root, width=1000, height=1000)
canvas.configure(bg = 'SkyBlue1')
canvas.bind("<Motion>", motion)
canvas.pack()

tick_agents()

root.mainloop()
