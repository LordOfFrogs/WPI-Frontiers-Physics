from vpython import *
#Web VPython 3.2

# Scene setup
scene.width = 800
scene.height = 800
scene.background = color.black
scene.autoscale = True

wtext(text='<h1 style="color:SlateBlue">1D Wave Simulation</h1><h3 style="color:SlateBlue">Tori Dell - Physics Frontiers 2023</h3>', pos=scene.title_anchor)

arrow(pos=vec(0,0,0), axis=vec(1,0,0), shaftwidth=0.1, color=color.red)
arrow(pos=vec(0,0,0), axis=vec(0,1,0), shaftwidth=0.1, color=color.blue)
arrow(pos=vec(0,0,0), axis=vec(0,0,1), shaftwidth=0.1, color=color.green)
label(pos=vec(1,0,0), line=False, box=False, text="X", height=10, opacity=0.2)
label(pos=vec(0,1,0), line=False, box=False, text="Y", height=10, opacity=0.2)
label(pos=vec(0,0,1), line=False, box=False, text="Z", height=10, opacity=0.2)

### INTERACTIVITY
warningText = wtext(text='<h2 style="color: orange">One or more of your variables is undefined! Press enter when entering variables.</h1>', pos=scene.title_anchor)
wtext(text='Raindrop Force: ')
rainFIn = slider(min=0, max=2, value=0.2, bind=checkVars)
wtext(text='\nAverage Raindrops Per Second: ')
rainPIn = slider(min=0, max=3, value=0.5, bind=checkVars)
wtext(text='\nRaindrop size: ')
spreadIn = slider(min=0.01, max=4, value=0.2, bind=checkVars)
wtext(text='\nDamping: ')
dampIn = slider(min=0, max=10, value=2, bind=checkVars)

def checkVars():
    global warningText, rainFIn, rainPIn
    global F_rain, p_rain, drop_spread, damping
    F_rain = rainFIn.value
    p_rain = rainPIn.value
    drop_spread = spreadIn.value
    damping = dampIn.value
    if None is not warningText:
        warningText.delete()
        warningText = None

### CONSTANTS
dt = 1/50 # time per incrament
length = 10
dx = 1/10
c = 5
rsq = (c*dt/dx)**2
nx = length / dx
F_rain = 0.2
p_rain = 0.5
drop_spread = 0.2
damping = 2

### SIMULATION VARIABLES
u = [ [], [] ]
line = curve(pos=[vec(0,0,0), vec(10,0,0)], radius=0.2)

### RUNNING MANAGEMENT
running = False

runButton = button(text="Run", bind=toggleRunning)
button(text="Restart", bind=restart)
button(text="Step", bind=loop)

def toggleRunning():
    global running
    running = not running
    runButton.text = "Pause" if running else "Run"
    
def restart():
    global running
    running = False
    runButton.text = "Run"
    start()

start()

while True:
    if running:
        loop()
    rate(1/dt)

### MAIN CODE
def start():
    ### ENTER CODE TO RUN ON START/RESET
    global u
    checkVars()
    u = [ [], [] ]
    for i in range(nx):
        u[0].append(0)
        u[1].append(0)

    line.clear()
    for i in range(len(u[1])):
        line.append(vec(i*dx-length/2,u[1][i], 0))

def loop():
    global u, line
    unext = []
    for x in range(1, nx-1):
        unext.append( (2*(1-rsq)*u[1][x]-u[0][x]+rsq*(u[1][x-1]+u[1][x+1])) * (1 - damping*dt) )
    u[0] = u[1]
    u[1] = [u[1][0],] + unext + [u[1][-1],]
    line.clear()
    for i in range(len(u[1])):
        line.append(vec(i*dx-length/2,u[1][i], 0))
    
    rainfall()
        
def rainfall():
    if random() < p_rain*dt:
        drop(floor(random()*(nx-2)+1))
        
def drop(n):
    for i in range(1,nx-1):
        u[1][i] -= F_rain * exp(-(1/drop_spread) * (i*dx - n*dx)**2)
