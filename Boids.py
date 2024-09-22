from vpython import *
#Web VPython 3.2
# Scene setup
scene.width = 800
scene.height = 800
scene.background = color.black
scene.autoscale = True

wtext(text='<h1 style="color:SlateBlue">Boids Simulation</h1><h3 style="color:SlateBlue">Tori Dell - Physics Frontiers 2023</h3>', pos=scene.title_anchor)

arrow(pos=vec(0,0,0), axis=vec(1,0,0), shaftwidth=0.1, color=color.red)
arrow(pos=vec(0,0,0), axis=vec(0,1,0), shaftwidth=0.1, color=color.blue)
arrow(pos=vec(0,0,0), axis=vec(0,0,1), shaftwidth=0.1, color=color.green)
label(pos=vec(1,0,0), line=False, box=False, text="X", height=10, opacity=0.2)
label(pos=vec(0,1,0), line=False, box=False, text="Y", height=10, opacity=0.2)
label(pos=vec(0,0,1), line=False, box=False, text="Z", height=10, opacity=0.2)

### INTERACTIVITY
warningText = wtext(text='<h2 style="color: orange">One or more of your variables is undefined! Press enter when entering variables.</h1>', pos=scene.title_anchor)
numBoidsInput = winput(prompt="# Boids", bind=checkVars)
wtext(text='\nCohesion Force')
cohesionInput = slider(bind=checkVars, value=0.05)
cohesionDistInput = winput(prompt='Cohesion Distance: ', bind=checkVars, text='9', number=9)

wtext(text='\nSeparation Force')
separationInput = slider(bind=checkVars, value=0.5)
separationDistInput = winput(prompt='Separation Distance: ', bind=checkVars, text='3', number=3)

wtext(text='\nAlignment Force')
alignInput = slider(bind=checkVars, value=0.5)
alignDistInput = winput(prompt='Alignment Distance: ', bind=checkVars, text='6', number=6)

speedInput = winput(prompt='\nSimulation speed: ', bind=checkVars, text='4', number=4)

def checkVars():
    global warningText, numBoidsInput, cohesionInput, cohesionDistInput, separationInput, separationDistInput, alignInput, alignDistInput, speedInput
    global cohesion, cohesionDist, separation, separationDist, align, alignDist, speed
    
    cohesion = cohesionInput.value
    cohesionDist = cohesionDistInput.number
    separation = separationInput.value
    separationDist = separationDistInput.number
    align = alignInput.value
    alignDist = alignDistInput.number
    speed = speedInput.number
            
    if None not in (warningText, numBoidsInput.number, cohesionInput.value, cohesionDistInput.number, separationInput.value, separationDistInput.number, alignInput.value, alignDistInput.number, speedInput.number):
        warningText.visible = False
        warningText = None

### CONSTANTS
dt = 1/50 # time per incrament
boid_radius = 0.1
boid_height = 0.4
bounds_length = 10
turn_force = 1
max_speed = 15

cylinder(pos=vec(-bounds_length/2, -bounds_length/2, -bounds_length/2), axis=vec(0,bounds_length,0), radius=0.2)
cylinder(pos=vec(bounds_length/2, -bounds_length/2, -bounds_length/2), axis=vec(0,bounds_length,0), radius=0.2)
cylinder(pos=vec(-bounds_length/2, -bounds_length/2, bounds_length/2), axis=vec(0,bounds_length,0), radius=0.2)
cylinder(pos=vec(bounds_length/2, -bounds_length/2, bounds_length/2), axis=vec(0,bounds_length,0), radius=0.2)
cylinder(pos=vec(-bounds_length/2, -bounds_length/2, -bounds_length/2), axis=vec(bounds_length,0,0), radius=0.2)
cylinder(pos=vec(-bounds_length/2, -bounds_length/2, -bounds_length/2), axis=vec(0,0,bounds_length), radius=0.2)
cylinder(pos=vec(bounds_length/2, -bounds_length/2, bounds_length/2), axis=vec(-bounds_length,0,0), radius=0.2)
cylinder(pos=vec(bounds_length/2, -bounds_length/2, bounds_length/2), axis=vec(0,0,-bounds_length), radius=0.2)
cylinder(pos=vec(-bounds_length/2, bounds_length/2, -bounds_length/2), axis=vec(bounds_length,0,0), radius=0.2)
cylinder(pos=vec(-bounds_length/2, bounds_length/2, -bounds_length/2), axis=vec(0,0,bounds_length), radius=0.2)
cylinder(pos=vec(bounds_length/2, bounds_length/2, bounds_length/2), axis=vec(-bounds_length,0,0), radius=0.2)
cylinder(pos=vec(bounds_length/2, bounds_length/2, bounds_length/2), axis=vec(0,0,-bounds_length), radius=0.2)

### SIMULATION VARIABLES
boids = []

def nearbyBoids(boid, distance):
    result = []
    for i in boids:
        if i is not boid and mag(i.pos-boid.pos) <= distance:
            result.append(i)
    return result
            
def cohesionForce(boid):
    global cohesion, cohesionDist
    nearby = nearbyBoids(boid, cohesionDist)
    force = vec(0,0,0)
    
    if len(nearby) == 0:
        return force
        
    for i in nearby:
        force += i.pos - boid.pos
    force /= len(nearby)
    return force*cohesion

def separationForce(boid):
    global separation, separationDist
    nearby = nearbyBoids(boid, separationDist)
    force = vec(0,0,0)
    
    if len(nearby) == 0:
        return force
        
    for i in nearby:
        force -= i.pos - boid.pos
        
    force /= len(nearby)
    return force*separation

def alignForce(boid):
    global align, alignDist
    nearby = nearbyBoids(boid, alignDist)
    force = vec(0,0,0)

    if len(nearby) == 0:
        return force
        
    for i in nearby:
        force += i.vel - boid.vel
    
    force /= len(nearby)
    return force*align
    
def boundsForce(boid):
    global turn_force
    force = vec(0,0,0)
    if boid.pos.x > bounds_length/2:
        force.x -= turn_force*(boid.pos.x-bounds_length/2)
    if boid.pos.y > bounds_length/2:
        force.y -= turn_force*(boid.pos.y-bounds_length/2)
    if boid.pos.x < -bounds_length/2:
        force.x += turn_force*(-bounds_length/2-boid.pos.x)
    if boid.pos.y < -bounds_length/2:
        force.y += turn_force*(-bounds_length/2-boid.pos.y)
    if boid.pos.z > bounds_length/2:
        force.z -= turn_force*(boid.pos.z-bounds_length/2)
    if boid.pos.z < -bounds_length/2:
        force.z += turn_force*(-bounds_length/2-boid.pos.z)

    return force
    

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
    global numBoidsInput, boids
    checkVars()
    
    for boid in boids:
        boid.visible = False
    
    boids = []
    for i in range(numBoidsInput.number):
        boids.append(cone(pos=vec.random()*bounds_length/2, radius=boid_radius, length=boid_height, color=color.white, vel=vec(0,0,0)))

def loop():
    global boids
    for boid in boids:
        boid.vel += cohesionForce(boid) + separationForce(boid) + alignForce(boid) + boundsForce(boid)
        if boid.vel.mag > max_speed:
            boid.vel.mag = max_speed
        boid.axis=boid.vel.norm()
        boid.pos += boid.vel * dt * speed
        