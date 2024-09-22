from vpython import *
#Web VPython 3.2

# Scene setup
scene.width = 700
scene.height = 700
scene.background = color.black
scene.autoscale = False
scene.range=10

wtext(text='<h1 style="color:SlateBlue">2D Wave Simulation</h1><h3 style="color:SlateBlue">Tori Dell - Physics Frontiers 2023</h3>', pos=scene.title_anchor)

arrow(pos=vec(0,0,0), axis=vec(1,0,0), shaftwidth=0.1, color=color.red)
arrow(pos=vec(0,0,0), axis=vec(0,1,0), shaftwidth=0.1, color=color.blue)
arrow(pos=vec(0,0,0), axis=vec(0,0,1), shaftwidth=0.1, color=color.green)
label(pos=vec(1,0,0), line=False, box=False, text="X", height=10, opacity=0.2)
label(pos=vec(0,1,0), line=False, box=False, text="Y", height=10, opacity=0.2)
label(pos=vec(0,0,1), line=False, box=False, text="Z", height=10, opacity=0.2)

### INTERACTIVITY
warningText = wtext(text='<h2 style="color: orange">One or more of your variables is undefined! Press enter when entering variables.</h1>', pos=scene.title_anchor)
wtext(text='Raindrop Force: ')
rainFIn = slider(min=0, max=2, value=0.3, bind=checkVars)
wtext(text='\nAverage Raindrops Per Second: ')
rainPIn = slider(min=0, max=3, value=2, bind=checkVars)
wtext(text='\nRaindrop size: ')
spreadIn = slider(min=0.01, max=4, value=0.2, bind=checkVars)
wtext(text='\nDamping: ')
dampIn = slider(min=0, max=15, value=2, bind=checkVars)
wtext(text='\nSpeed: ')
speedIn = slider(min=0.01, max=10, value=7, bind=checkVars)

def checkVars():
    global warningText, rainFIn, rainPIn, speedIn
    global F_rain, p_rain, drop_spread, damping, c, alpha
    F_rain = rainFIn.value
    p_rain = rainPIn.value
    drop_spread = spreadIn.value
    damping = dampIn.value
    c=speedIn.value
    alpha = min((c*dt/dx)**2, 1)
    if None is not warningText:
        warningText.delete()
        warningText = None

### CONSTANTS
dt = 1/50 # time per incrament
length = 10
dx = 1/10
c = 7
nx = length / dx
nz = length / dx
F_rain = 0.2
p_rain = 0.5
drop_spread = 0.2
damping = 2
alpha = min((c*dt/dx)**2, 1)

### SIMULATION VARIABLES
u = [ [], [], [] ]

verts = []
for x in range(nx+1):
    verts.append([])
    for z in range(nz+1):
        verts[x].append(vertex(pos=vec(-length/2+x*dx,0,-length/2+z*dx), color=color.gray(0.5+random()*0.5)))

for x in range(nx):
    for z in range(nz):
        quad(vs=[verts[x][z], verts[x][z+1], verts[x+1][z+1], verts[x+1][z]])

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
    u = [ [], [], [] ]
    for i in range(nx):
        u[0].append([])
        u[1].append([])
        u[2].append([])
        for j in range(nz):
            u[0][i].append(0)
            u[1][i].append(0)
            u[2][i].append(0)

def loop():
    global u, alpha
    u[2] = deepcopy(u[1])
    u[1] = deepcopy(u[0])

    for i in range(1, nx-1):
        for j in range(1, nz-1):
            u[0][i][j] = u[0][i][j] + alpha * (u[1][i-1][j]+u[1][i+1][j]+u[1][i][j-1]+u[1][i][j+1]-4*u[1][i][j])/4 + u[1][i][j]-u[2][i][j]
            u[0][i][j] = u[0][i][j]*(1-damping*dt)
    
    rainfall()
    updateSurface()
        
def rainfall():
    if random() < p_rain*dt:
        drop(floor(random()*(nx-2)+1), floor(random()*(nz-2)+1))
        
     
def drop(x, z):
    global u

    for i in range(1,nx-1):
        for j in range(1, nz-1):
            u[0][i][j] = u[0][i][j] - F_rain * exp(-(1/drop_spread) * (i*dx - x*dx)**2) * exp(-(1/drop_spread) * (j*dx - z*dx)**2)

def updateSurface():
    for i in range(nx):
        for j in range(nz):
            verts[i][j].color = color.red*(u[0][i][j]+1/2)+color.blue + vector.random()/100
            verts[i][j].pos.y = u[0][i][j]
            
def deepcopy(arr):
    if not isinstance(arr, list):
        return arr
    if not isinstance(arr[0], list):
        return arr.copy()
    result = []
    for i in arr:
        result.append(deepcopy(i))
    return result
        
