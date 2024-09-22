from vpython import *
#Web VPython 3.2
# Scene setup
scene.width = 800
scene.height = 800
scene.background = color.black
scene.autoscale = True

wtext(text='<h1 style="color:SlateBlue">Collision Simulation</h1><h3 style="color:SlateBlue">Tori Dell - Physics Frontiers 2023</h3>', pos=scene.title_anchor)

arrow(pos=vec(0,0,0), axis=vec(1,0,0), shaftwidth=0.1, color=color.red)
arrow(pos=vec(0,0,0), axis=vec(0,1,0), shaftwidth=0.1, color=color.blue)
arrow(pos=vec(0,0,0), axis=vec(0,0,1), shaftwidth=0.1, color=color.green)
label(pos=vec(1,0,0), line=False, box=False, text="X", height=10, opacity=0.2)
label(pos=vec(0,1,0), line=False, box=False, text="Y", height=10, opacity=0.2)
label(pos=vec(0,0,1), line=False, box=False, text="Z", height=10, opacity=0.2)

### INTERACTIVITY
warningText = wtext(text='<h2 style="color: orange">One or more of your variables is undefined! Press enter when entering variables.</h1>', pos=scene.title_anchor)
numBallsIn = winput(prompt="Number of balls: ", text="10", number=10, bind=checkVars)
boundsIn = winput(prompt="Bounds size: ", text="10", number=10, bind=checkVars)

def checkVars():
    global warningText, numBallsIn, boundsIn
    global bounds_length, initNum
    initNum = numBallsIn.number
    bounds_length = boundsIn.number
    if None not in (warningText, numBallsIn.number, boundsIn.number):
        warningText.delete()
        warningText = None

### CONSTANTS
dt = 1/50 # time per incrament
g = 9.8 # m/s^2
elasticity_ball = 0.9
elasticity_wall = 0.6
rolling_friction = 0.5
v0_rand = 5
rad_min = 0.1
rad_max = 1
mass_min = 0.1
mass_max = 10

bounds_rad = 0.2
bounds = None
floor = None

def drawBounds(len, rad):
    global bounds, floor
    _a = cylinder(pos=vec(-bounds_length/2, -bounds_length/2, -bounds_length/2), axis=vec(0,bounds_length,0), radius=bounds_rad)
    _b = cylinder(pos=vec(bounds_length/2, -bounds_length/2, -bounds_length/2), axis=vec(0,bounds_length,0), radius=bounds_rad)
    _c = cylinder(pos=vec(-bounds_length/2, -bounds_length/2, bounds_length/2), axis=vec(0,bounds_length,0), radius=bounds_rad)
    _d= cylinder(pos=vec(bounds_length/2, -bounds_length/2, bounds_length/2), axis=vec(0,bounds_length,0), radius=bounds_rad)
    _e=cylinder(pos=vec(-bounds_length/2, -bounds_length/2, -bounds_length/2), axis=vec(bounds_length,0,0), radius=bounds_rad)
    _f=cylinder(pos=vec(-bounds_length/2, -bounds_length/2, -bounds_length/2), axis=vec(0,0,bounds_length), radius=bounds_rad)
    _g=cylinder(pos=vec(bounds_length/2, -bounds_length/2, bounds_length/2), axis=vec(-bounds_length,0,0), radius=bounds_rad)
    _h=cylinder(pos=vec(bounds_length/2, -bounds_length/2, bounds_length/2), axis=vec(0,0,-bounds_length), radius=bounds_rad)
    _i=cylinder(pos=vec(-bounds_length/2, bounds_length/2, -bounds_length/2), axis=vec(bounds_length,0,0), radius=bounds_rad)
    _j=cylinder(pos=vec(-bounds_length/2, bounds_length/2, -bounds_length/2), axis=vec(0,0,bounds_length), radius=bounds_rad)
    _k=cylinder(pos=vec(bounds_length/2, bounds_length/2, bounds_length/2), axis=vec(-bounds_length,0,0), radius=bounds_rad)
    _l=cylinder(pos=vec(bounds_length/2, bounds_length/2, bounds_length/2), axis=vec(0,0,-bounds_length), radius=bounds_rad)
    floor = extrusion(path=[vec(0,-bounds_length/2,0), vec(0,-bounds_length/2-0.1, 0)], shape=shapes.rectangle(width=bounds_length, height=bounds_length), color=vec(40, 37, 33)/255)
    bounds = compound([_a,_b,_c,_d,_e,_f,_g,_h,_i,_j,_k,_l])

### SIMULATION VARIABLES
balls = []

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
    if bounds is not None:
        bounds.visible = False
    if floor is not None:
        floor.visible = False
    drawBounds(bounds_length, bounds_rad)
    
    global balls
    for ball in balls:
        ball.visible = False
    balls = []
    for i in range(initNum):
        balls.append(sphere(radius=random()*(rad_max-rad_min)+rad_min, vel=vector.random()*v0_rand, mass = random()*(mass_max-mass_min)+mass_min ))
        vol = 4/3 * pi * balls[i].radius**3
        vol_min = 4/3 * pi * rad_min
        vol_max = 4/3 * pi * rad_min

        balls[i].color = vec(( balls[i].mass /vol - mass_min/vol_max) / (mass_max/vol_min - mass_min/vol_max), 1, 1)
        
        posSet = False
        while not posSet:
            balls[i].pos = vector.random()*(bounds_length/2-balls[i].radius)
            posSet=True
            for ball in balls:
                if ball is not balls[i] and mag(ball.pos - balls[i].pos) < ball.radius + balls[i].radius:
                    posSet=False

def loop():
    for ball in balls:
        ballCollisions(ball)
        boundsCollisions(ball)
        
        ball.vel.y -= g*dt
        ball.pos += ball.vel*dt
        
def ballCollisions(ball):
    for other in balls:
        if other is not ball and mag(ball.pos - other.pos) < ball.radius + other.radius:
            direction = norm(ball.pos - other.pos)
            force = dot(ball.vel, -direction) + dot(other.vel, direction)
            force = max(force, 0) * ball.mass / (ball.mass+other.mass)
            
            ball.vel += direction * force * elasticity_ball**2
            ball.pos = other.pos + direction * (ball.radius+other.radius)
            
def boundsCollisions(ball):
    if ball.pos.x+ball.radius > bounds_length/2:
        ball.vel.x*=-elasticity_ball*elasticity_wall
        ball.pos.x = bounds_length/2 - ball.radius
    if ball.pos.y+ball.radius > bounds_length/2:
        ball.vel.y*=-elasticity_ball*elasticity_wall
        ball.pos.y = bounds_length/2 - ball.radius
    if ball.pos.x-ball.radius < -bounds_length/2:
        ball.vel.x*=-elasticity_ball*elasticity_wall
        ball.pos.x = -bounds_length/2 + ball.radius
    if ball.pos.y-ball.radius < -bounds_length/2:
        ball.vel.y*=-elasticity_ball*elasticity_wall
        if abs(ball.vel.y) < 0.1:
            ball.vel.x *= 1-rolling_friction*dt
            ball.vel.z *= 1-rolling_friction*dt
        ball.pos.y = -bounds_length/2 + ball.radius
    if ball.pos.z+ball.radius > bounds_length/2:
        ball.vel.z*=-elasticity_ball*elasticity_wall
        ball.pos.z = bounds_length/2 - ball.radius
    if ball.pos.z-ball.radius < -bounds_length/2:
        ball.vel.z*=-elasticity_ball*elasticity_wall
        ball.pos.z = -bounds_length/2 + ball.radius