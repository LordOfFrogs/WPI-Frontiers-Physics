from vpython import *
#Web VPython 3.2

# Scene setup
scene.width = 800
scene.height = 800
scene.background = color.black
scene.autoscale = True

wtext(text='<h1 style="color:SlateBlue">Orbital Dynamics Simulation</h1><h3 style="color:SlateBlue">Tori Dell - Physics Frontiers 2023</h3>', pos=scene.title_anchor)

arrow(pos=vec(0,0,0), axis=vec(1,0,0), shaftwidth=0.1, color=color.red)
arrow(pos=vec(0,0,0), axis=vec(0,1,0), shaftwidth=0.1, color=color.blue)
arrow(pos=vec(0,0,0), axis=vec(0,0,1), shaftwidth=0.1, color=color.green)
label(pos=vec(1,0,0), line=False, box=False, text="X", height=10, opacity=0.2)
label(pos=vec(0,1,0), line=False, box=False, text="Y", height=10, opacity=0.2)
label(pos=vec(0,0,1), line=False, box=False, text="Z", height=10, opacity=0.2)

### INTERACTIVITY
warningText = wtext(text='<h2 style="color: orange">One or more of your variables is undefined! Press enter when entering variables.</h2>', pos=scene.title_anchor)

speedInput = winput(bind=checkVars, prompt="Simulation Speed: ")

def checkVars():
    global warningText
    if warningText is not None and speedInput.number is not None:
        warningText.delete()
        warningText = None

### SIMULATION VARIABLES
sun = sphere(pos=vec(0, 0, 0), radius=696.34e+6, color=color.yellow, mass=1.989e+30)
earth = sphere(radius=6.371e+6, color=color.blue, a=1.496e+11, mass=5.9722e+24, vel=vec(0,0,0), acc=vec(0,0,0), F=vec(0,0,0))
mars = sphere(radius=3.3895e+6, color=color.red, a=2.2739e+11, mass=6.39e+23, vel=vec(0,0,0), acc=vec(0,0,0), F=vec(0,0,0))

label(pos=sun.pos, line=True, box=True, text="Sun", height=10, opacity=0.2)
earthLabel = label(pos=earth.pos, line=True, box=True, text="Earth", height=10, opacity=0.2)
marsLabel = label(pos=mars.pos, line=True, box=True, text="Mars", height=10, opacity=0.2)

attach_trail(earth, radius=earth.radius*400, retain=500)
attach_trail(mars, radius=mars.radius*400, retain=500)

attach_arrow(earth, "vel", scale=1e+6, shaftwidth=earth.radius*400, color=color.green)
attach_arrow(mars, "vel", scale=1e+6, shaftwidth=mars.radius*400, color=color.green)

attach_arrow(earth, "acc", scale=1e+13, shaftwidth=earth.radius*400, color=color.red)
attach_arrow(mars, "acc", scale=1e+13, shaftwidth=mars.radius*400, color=color.red)

sat_arrow = arrow(pos=earth.pos, color=color.yellow, shaftwidth=earth.radius*400)

satellite = sphere(pos=sun.pos+vec(0,0,1), vel=vec(0,0,0), acc=vec(0,0,0), a=(earth.a+mars.a)/2)
sat_trail=attach_trail(satellite, radius=mars.radius*400)
sat_label = label(pos=satellite.pos, line=True, box=True, text="Probe", height=10, opacity=0.2)

def orbitalPeriod(a, M):
    return sqrt(a**3 * 4*pi**2 / (G*M))
    
def orbitalVel(M, a):
    return sqrt(G*M / a)
    
def F_grav(m1, m2, r):
    return G*(m1*m2)/(r**2)

def acc_grav(M, r):
    return G*M/r**2

### CONSTANTS
dt = 1/50 # time per incrament

G = 6.674e-11
sat_angle = pi - orbitalPeriod(satellite.a, sun.mass) / orbitalPeriod(mars.a, sun.mass)*pi
sat_eccentricity = 1 - earth.a/satellite.a

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
    checkVars()
    earth.pos = vec(earth.a, 0, 0)
    mars.pos = vec(mars.a, 0, 0)
    
    earth.vel = vec(0, 0, -orbitalVel(sun.mass, earth.a))
    mars.vel = vec(0, 0, -orbitalVel(sun.mass, mars.a))

def loop():
    earth.F = (sun.pos-earth.pos).norm()*F_grav(earth.mass, sun.mass, (sun.pos-earth.pos).mag)
    mars.F = (sun.pos-mars.pos).norm()*F_grav(mars.mass, sun.mass, (sun.pos-mars.pos).mag)
    
    earth.acc = earth.F/earth.mass
    mars.acc = mars.F/mars.mass
    satellite.acc = (sun.pos-satellite.pos).norm()*acc_grav(sun.mass, (sun.pos-satellite.pos).mag)
    
    earth.vel += earth.acc*dt*speedInput.number
    mars.vel += mars.acc*dt*speedInput.number
    satellite.vel += satellite.acc*dt*speedInput.number
    
    earth.pos += earth.vel*dt*speedInput.number
    mars.pos += mars.vel*dt*speedInput.number
    satellite.pos+= satellite.vel*dt*speedInput.number
    
    earthLabel.pos = earth.pos
    marsLabel.pos = mars.pos
    sat_arrow.pos = earth.pos
    sat_label.pos = satellite.pos
    
    sat_arrow.axis = rotate(earth.vel.norm(), -sat_angle, axis=vec(0,1,0)) * 1e+11
    
    if dot(sat_arrow.axis.norm(), (mars.pos-earth.pos).norm()) > 0.99:
        satellite.pos=earth.pos
        sat_trail.clear()
        satellite.vel = vec(-earth.acc.z, earth.acc.y, earth.acc.x).norm() * orbitalVel(sun.mass, satellite.a) * sqrt( (1+sat_eccentricity) / (1-sat_eccentricity) )
        