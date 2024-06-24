import os
import random
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import Canvas, HORIZONTAL

import model.predator
from constants import *
from model.couzin_agent import CouzinAgent
from model.predator import Predator
from model.task import Task

# increments each time we start a new run
executionNo = 0

def tick_agents(myExecutionNo):
    global agents, tasks, predators, ticks_elapsed, ticksDisplay, time_start, timeDisplay, sliderTPS, executionNo
    # a new execution has been started, we are no longer needed
    if myExecutionNo != executionNo:
        return

    # remove tasks with scope 0
    tasks[:] = filter(lambda t: t.scope > 0, tasks)

    for agent in agents:
        agent.tick(agents, predators, tasks)
    for pred in predators:
        pred.tick(agents, predators, tasks)
    drawThread = threading.Thread(target=render_map)
    drawThread.start()

    ticks_elapsed += 1
    ticksDisplay.config(text = str(ticks_elapsed))
    timeDisplay.config(text = f'{(datetime.now() - time_start).total_seconds():.2f} seconds')
    actualTPSDisplay.config(text = f'{ticks_elapsed/(datetime.now() - time_start).total_seconds():.2f}')

    if len(tasks) == 0:
        printAndLog(f'{ticks_elapsed},{"PRED" if enablePredator.get()==1 else "PAR"},{time_start},{time_start.microsecond},({sliderZoneRepulsion.get()},{sliderZoneOrientation.get()},{sliderZoneAttraction.get()},{sliderZoneAttractionTask.get()},{sliderAgentNum.get()},{sliderTaskNum.get()},{sliderTaskScope.get()},{sliderPredatorRepulsionRadius.get()},{sliderPredatorRepulsionStrength.get()})')
        if enablePredator.get() == 0:
            print('Restarting...')
            generateAndStart()
    else:
        tickThread = threading.Timer(1.0 / sliderTPS.get(), tick_agents, [myExecutionNo])
        tickThread.start()


def printAndLog(string):
    print(string)
    with open("results.csv", "a") as myfile:
        myfile.write(string)
        myfile.write('\n')

def render_map():
    global agents, predators, tasks, canvas, drawn_objects
    for agent in agents:
        canvas.coords(drawn_objects[agent][0], agent.x - AGENT_SIZE, agent.y - AGENT_SIZE, agent.x + AGENT_SIZE, agent.y + AGENT_SIZE)
        canvas.coords(drawn_objects[agent][1], agent.x, agent.y, agent.x + int(agent.direction[0] * 20),
                           agent.y + int(agent.direction[1] * 20))

    for p in predators:
        canvas.coords(drawn_objects[p], p.x - PREDATOR_SIZE, p.y - PREDATOR_SIZE, p.x + PREDATOR_SIZE, p.y + PREDATOR_SIZE)

    for t in tasks:
        size = (t.scope/sliderTaskScope.get()) * TASK_SIZE
        # size of task is equal to its scope
        if size > 0:
            canvas.coords(drawn_objects[t], t.x - size, t.y - size, t.x + size, t.y + size)
        else:
            canvas.delete(drawn_objects[t])


drawn_objects = {}


def render_map_first():
    global agents, predators, tasks, canvas, drawn_objects
    canvas.delete("all")
    drawn_objects = {}
    for agent in agents:
        agent_circle = canvas.create_oval(agent.x - AGENT_SIZE, agent.y - AGENT_SIZE, agent.x + AGENT_SIZE, agent.y + AGENT_SIZE,
                           fill='blue4')
        agent_heading = canvas.create_line(agent.x, agent.y, agent.x + int(agent.direction[0] * 20),
                           agent.y + int(agent.direction[1] * 20))
        drawn_objects[agent] = (agent_circle, agent_heading)

    for p in predators:
        drawn_objects[p] = canvas.create_oval(p.x - PREDATOR_SIZE, p.y - PREDATOR_SIZE, p.x + PREDATOR_SIZE, p.y + PREDATOR_SIZE,
                           fill='red2')

    for t in tasks:
        size = (t.scope/sliderTaskScope.get()) * TASK_SIZE
        # size of task is equal to its scope
        drawn_objects[t] = canvas.create_oval(t.x - size, t.y - size, t.x + size, t.y + size, fill='green2')


def motion(event):
    model.predator.target_x = canvas.canvasx(event.x)
    model.predator.target_y = canvas.canvasy(event.y)

def createConfigSlider(label, min, max, row, col, default):
    labelNew = tk.Label(root, text=f"{label}: ")
    labelNew.grid(row=row, column=col)
    sliderNew = tk.Scale(root, from_=min, to=max, orient=HORIZONTAL)
    sliderNew.grid(row=row, column=col+1)
    sliderNew.set(default)
    return sliderNew

def generateAndStart():
    global agents, tasks, predators, time_start, ticks_elapsed, sliderAgentNum, sliderTaskNum, sliderTaskScope, executionNo
    agents = []
    time_start = datetime.now()
    random.seed(time_start.microsecond)
    for i in range(int(sliderAgentNum.get())):
        agents.append(
            CouzinAgent(
                random.randrange(int(MAP_SIZE_X/2-25), int(MAP_SIZE_X/2+25)),
                random.randrange(int(MAP_SIZE_Y/2-25), int(MAP_SIZE_Y/2+25)),
                (random.uniform(-1, 1), random.uniform(-1, 1)),
                3,
                int(sliderZoneRepulsion.get()),
                int(sliderZoneOrientation.get()),
                int(sliderZoneAttraction.get())
            )
        )

    tasks = []
    for i in range(int(sliderTaskNum.get())):
        tasks.append(
            Task(
                random.randrange(MAP_INNER_BORDER, MAP_SIZE_X - MAP_INNER_BORDER),
                random.randrange(MAP_INNER_BORDER, MAP_SIZE_Y - MAP_INNER_BORDER),
                int(sliderTaskScope.get()),
                TASK_ATTRACTION_RADIUS,
                TASK_ACTION_RADIUS,
                TASK_FORCE_SCALE
            )
        )

    predators = []
    if enablePredator.get() == 1:
        predators = [Predator(500, 500, PREDATOR_SPEED, int(sliderPredatorRepulsionRadius.get()), int(sliderPredatorRepulsionStrength.get()))]

    ticks_elapsed = 0
    executionNo += 1
    render_map_first()
    tick_agents(executionNo)

def setParPreset():
    sliderZoneRepulsion.set(R_ZONE_RADIUS_PAR)
    sliderZoneOrientation.set(O_ZONE_RADIUS_PAR)
    sliderZoneAttraction.set(A_ZONE_RADIUS_PAR)
    enablePredator.set(0)
def setPredPreset():
    sliderZoneRepulsion.set(R_ZONE_RADIUS_PRED)
    sliderZoneOrientation.set(O_ZONE_RADIUS_PRED)
    sliderZoneAttraction.set(A_ZONE_RADIUS_PRED)
    enablePredator.set(1)


printAndLog("program started at " + str(datetime.now()))

agents = []
tasks = []
predators = []
ticks_elapsed = 0
time_start = datetime.now()

root = tk.Tk()
root.geometry(f'{MAP_SIZE_X+50}x{MAP_SIZE_Y + 200}')

ticksLabel = tk.Label(root, text = "Ticks run: ")
ticksDisplay = tk.Label(root, text ="0")
ticksLabel.grid(row=0, column=0)
ticksDisplay.grid(row=0, column=1)

timeLabel = tk.Label(root, text = "Time elapsed: ")
timeDisplay = tk.Label(root, text = "0")
timeLabel.grid(row=1, column=0)
timeDisplay.grid(row=1, column=1)

actualTPSLabel = tk.Label(root, text = "actual TPS: ")
actualTPSDisplay = tk.Label(root, text = "0")
actualTPSLabel.grid(row=2, column=0)
actualTPSDisplay.grid(row=2, column=1)

sliderZoneRepulsion = createConfigSlider("Repulsion Zone", 0, 200, 0, 2, R_ZONE_RADIUS_PRED)
sliderZoneOrientation = createConfigSlider("Orientation Zone", 0, 200, 1, 2, O_ZONE_RADIUS_PRED)
sliderZoneAttraction = createConfigSlider("Attraction Zone", 0, 200, 2, 2, A_ZONE_RADIUS_PRED)
sliderZoneAttractionTask = createConfigSlider("Task Attraction Zone", 0, 200, 3, 2, TASK_ATTRACTION_RADIUS)

enablePredator = tk.IntVar()
enablePredator.set(1)
predatorOnRadio = tk.Radiobutton(root, text="Predator ON", variable=enablePredator, value=1)
predatorOffRadio = tk.Radiobutton(root, text="Predator OFF", variable=enablePredator, value=0)
predatorOnRadio.grid(row=2, column=6)
predatorOffRadio.grid(row=3, column=6)

sliderTPS = createConfigSlider("TPS", 5, 144, 0, 4, TICKS_PER_SECOND)
sliderAgentNum = createConfigSlider("Agents", 1, 30, 1, 4, AGENT_AMOUNT)
sliderTaskNum = createConfigSlider("Tasks", 1, 40, 2, 4, TASK_AMOUNT)
sliderTaskScope = createConfigSlider("Task Scope", 5, 3000, 3, 4, TASK_SCOPE)
sliderPredatorRepulsionRadius = createConfigSlider("Predator Repulsion Zone", 0, 200, 0, 6, PREDATOR_RADIUS)
sliderPredatorRepulsionStrength = createConfigSlider("Predator Repulsion Force", 0, 100, 1, 6, PREDATOR_FORCE)

startButton = tk.Button(root, text="Start", command=generateAndStart)
startButton.grid(row = 3, column = 0)

presetButtonPred = tk.Button(root, text="PRED Preset", command=setPredPreset)
presetButtonPred.grid(row = 2, column = 7)

presetButtonPar = tk.Button(root, text="PAR Preset", command=setParPreset)
presetButtonPar.grid(row = 3, column = 7)

canvas = Canvas(root, width=MAP_SIZE_X, height=MAP_SIZE_Y)
canvas.configure(bg='SkyBlue1')
canvas.bind("<Motion>", motion)
canvas.grid(row=4, column=0, columnspan=10)

root.mainloop()
os._exit(1)
