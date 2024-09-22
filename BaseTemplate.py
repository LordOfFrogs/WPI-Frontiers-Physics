from vpython import *
#Web VPython 3.2

# Scene setup
scene.width = 800
scene.height = 800
scene.background = color.black
scene.autoscale = True

arrow(pos=vec(0,0,0), axis=vec(1,0,0), shaftwidth=0.1, color=color.red)
arrow(pos=vec(0,0,0), axis=vec(0,1,0), shaftwidth=0.1, color=color.blue)
arrow(pos=vec(0,0,0), axis=vec(0,0,1), shaftwidth=0.1, color=color.green)
label(pos=vec(1,0,0), line=False, box=False, text="X", height=10, opacity=0.2)
label(pos=vec(0,1,0), line=False, box=False, text="Y", height=10, opacity=0.2)
label(pos=vec(0,0,1), line=False, box=False, text="Z", height=10, opacity=0.2)

### INTERACTIVITY
warningText = wtext(text='<h2 style="color: orange">One or more of your variables is undefined! Press enter when entering variables.</h1>', pos=scene.title_anchor)

def checkVars():
    global warningText
    if None not in (warningText):
        warningText.delete()
        warningText = None

### CONSTANTS
dt = 1/50 # time per incrament

### SIMULATION VARIABLES


### RUNNING MANAGEMENT
running = False

runButton = button(text="Run", bind=toggleRunning)
button(text="Restart", bind=restart)

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
    checkVars()
    pass

def loop():
    pass ### ENTER CODE TO RUN EVERY LOOP