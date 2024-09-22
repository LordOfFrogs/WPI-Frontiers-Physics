from vpython import *
#Web VPython 3.2

# Scene setup
scene.width = 600
scene.height = 600
scene.background = color.black
scene.range = 100
scene.autoscale = False

wtext(text='<h1 style="color:SlateBlue">Projectile Motion Simulation</h1><h3 style="color:SlateBlue">Tori Dell - Physics Frontiers 2023</h3>', pos=scene.title_anchor)

### INTERACTIVITY
warningText = wtext(text='<h2 style="color: orange">One or more of your variables is undefined! Press enter when entering variables.</h1>', pos=scene.title_anchor)

gInput = winput(prompt="Gravity (m/s^2)", bind=updateG, type = "numeric", text="9.8", number=9.8)
v0xInput = winput(prompt="Initial Velocity (m/s): x", bind=updateV0, type = "numeric", text="20", number=20)
v0yInput = winput(prompt="y", bind=updateV0, type = "numeric", text="0", number=0)
v0zInput = winput(prompt="z", bind=updateV0, type = "numeric", text="0", number=0)

v0 = vec(0,0,0)

def updateG():
    global g
    g = gInput.number
    checkVars()
    
def updateV0():
    global v0
    v0 = vec(v0xInput.number, v0yInput.number, v0zInput.number)
    checkVars()

def checkVars():
    global g, v0, warningText
    if None not in (g, v0, warningText) and None not in (v0.x, v0.y, v0.z):
        warningText.delete()
        warningText = None
        start()


### CONSTANTS
dt = 1/50 # time per incrament
bounceDamp = 0.9

### SIMULATION VARIABLES
tableTop = box(pos=vec(0, 0, 0), size=vec(100, 10, 50), color=color.white)

tableLeg1 = box(size=vec(10, 30, 10), color=color.white)
tableLeg1.pos = vec(tableTop.size.x/2-tableLeg1.size.x/2, -tableLeg1.size.y/2, tableTop.size.z/2-tableLeg1.size.z/2)

tableLeg2 = box(size=vec(10, 30, 10), color=color.white)
tableLeg2.pos = vec(tableTop.size.x/2-tableLeg2.size.x/2, -tableLeg2.size.y/2, -tableTop.size.z/2+tableLeg2.size.z/2)

tableLeg3 = box(size=vec(10, 30, 10), color=color.white)
tableLeg3.pos = vec(-tableTop.size.x/2+tableLeg3.size.x/2, -tableLeg3.size.y/2, tableTop.size.z/2-tableLeg3.size.z/2)

tableLeg4 = box(size=vec(10, 30, 10), color=color.white)
tableLeg4.pos = vec(-tableTop.size.x/2+tableLeg4.size.x/2, -tableLeg4.size.y/2, -tableTop.size.z/2+tableLeg4.size.z/2)

table = compound([tableTop, tableLeg1, tableLeg2, tableLeg3, tableLeg4], pos=tableTop.pos)

ball = sphere(pos=vec(-20, 40, 0), radius=5, color=color.green, vel=vec(0,0,0), acc=vec(0, 0, 0))
velArrow = attach_arrow(ball, "vel", scale=0.3, shaftwidth=1)
accArrow = attach_arrow(ball, "acc", scale=0.3, shaftwidth=1, color=color.yellow)
ballTrail = attach_trail(ball)

### RUNNING MANAGEMENT
running = False

runButton = button(text="Run", bind=toggleRunning)
button(text="Restart", bind=restart)
button(text="Reset Trails", bind=resetTrails)

def toggleRunning():
    global running
    running = not running
    runButton.text = "Pause" if running else "Run"
    
def restart():
    global running
    running = False
    runButton.text = "Run"
    ballTrail.stop()
    start()

def resetTrails():
    ballTrail.clear()

start()

while True:
    if running:
        loop()
    rate(1/dt)

### MAIN CODE
def start():
    updateG()
    updateV0()
    
    ball.pos=vec(-20, 40, 0)
    ball.vel = v0
    ball.acc.y = -g
    ballTrail.start()

def loop():
    if (ball.pos.y-ball.radius <= table.pos.y+table.size.y/2 and \
        ball.pos.x < table.pos.x+table.size.x/2 and ball.pos.x > table.pos.x-table.size.x/2 and \
        ball.pos.z < table.pos.z+table.size.z/2 and ball.pos.z > table.pos.z-table.size.z/2):
            
        ball.pos.y = table.pos.y+table.size.y/2+ball.radius
        ball.vel.y = abs(ball.vel.y)
        ball.vel *= bounceDamp
    
    ball.vel += ball.acc
    ball.pos += ball.vel * dt