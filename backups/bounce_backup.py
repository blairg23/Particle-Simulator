#!/usr/bin/python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, time
from pylab import *
from  particles import *
from particleInitialize import *

# This program is a 'driver' for a simple simulation of partilces in a box with
# periodic boundary conditions. Your objective will be to complete the code here
# so that you can 'see' the particles with OpenGL.

# Ball parameters

##color   = False
##radius  = 0.2
##x, y    = (0, 0)   # position
##vx, vy  = (0, 0)   # velocity
##gravity = 0.00001  # acceleration
##elasticity = 1     # damping
##theta, phi = 0, 0

#############################

tStart = t0 = time.time()

dt = 0.1   # Time step taken by the time integration routine.
L = 10.    # Size of the box.
wSize = 800 # Size of the window.
t = 0      # Initial time

# Particle update data:
COUNT = 1                    # Number of time steps computed
UPDATE_FRAMES = 2            # How often to redraw screen
ADD_PARTICLE_INTERVAL = 10   # How often to add a new particle

# How resolved are the spheres?
STACKS = 25
SLICES = 25

# Instantiate the forces function between particles
f = GranularMaterialForce()
# Create some particles and a box
p = Particles(L,f,periodicY=0)
particleInitialize(p,'one',L)
# Instantiate Integrator
integrate = VerletIntegrator(dt)

#Global variables:
rotateX = 0
rotateY = 0
rotateZ = 0
translateZ = 0
lightMover = 0

color = True
teapot = False
sphere = True
donut = False

velocity = True #To start with white background
radius = False
greyScale = False
alpha = 1.0#How transparent the spheres are

def init():
    # Initialization
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(100,0)
    glutInitWindowSize(wSize, wSize);
    glutCreateWindow("Large Hadron Collider")
    glClearColor(1.0,1.0,1.0,1.0)
    
    glEnable(GL_DEPTH_TEST)
    
    # Register Call-back Functions
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special)
    glutDisplayFunc(display)

    # Lighting Parameters
    glEnable(GL_POLYGON_OFFSET_FILL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
    glPolygonOffset(1.0, 1.0)        # a wireframe on top of filled polygons.

    #glMatrixMode(GL_MODELVIEW) #for modelview matrix
    #glMatrixMode(GL_PROJECTION) #for projection matrix
    glViewport(0,0,wSize,wSize)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-L, L, -L, L, -L, L)
    #glMatrixMode(GL_MODELVIEW)
    
    #Blending color on the spheres
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);    


##### Display Call-back Function ####

def display():
    global velocity, radius, alpha, greyScale, lightMover
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW) #Manipulate the model matrix from here on out
    
    #Fancy custom zooming and rotation:
    glLoadIdentity()
    glTranslate(0, 0, translateZ)
    glRotatef(rotateX, 1.0, 0.0, 0.0)
    glRotatef(rotateY, 0.0, 1.0, 0.0)
    glRotatef(rotateZ, 0.0, 0.0, 1.0)
    #glLight(GL_LIGHT0, GL_POSITION, [rotateX, rotateY, rotateZ, 1.0]);
    glLight(GL_LIGHT0, GL_POSITION, [lightMover, lightMover, lightMover, 1.0])    

    # no idea
    glEnable(GL_CULL_FACE)
    glEnable(GL_POLYGON_SMOOTH)
    glCullFace(GL_BACK)

    alpha = alpha
    minVel = 9999
    maxVel = 0.0
    for i in range(p.N):
        #Define the particle properties:
        rad = p.r[i]
        velX = p.vx[i]
        velY = p.vy[i]
        velZ = p.vz[i]        
        #Define the colors:
        
        #DEFAULT COLORS:
        red = 0
        green = 0
        blue = 0
        if velocity:
            glClearColor(1.0,1.0,1.0,1.0)
            red = velX
            green = velY
            blue = velZ            
#########This is cool if you want to see the max or min velocities in action: #################
##            if velX > maxVel:
##                red = velX
##                maxVel = velX
##                print "Current Max Velocity is: X-Velocity (RED) at " + str(maxVel)
##            elif velX < minVel:
##                red = 1/velX
##                minVel = velX
##                print "Current Min Velocity is: X-Velocity (RED) at " + str(minVel)
##            elif velY > maxVel:
##                green = velY
##                maxVel = velY
##                print "Current Max Velocity is: Y-Velocity (GREEN) at " + str(maxVel)
##            elif velY < minVel:
##                green = 1/velY
##                minVel = velY
##                print "Current Min Velocity is: Y-Velocity (GREEN) at " + str(minVel)
##            elif velZ > maxVel:
##                blue = velZ
##                maxVel = velZ
##                print "Current Max Velocity is: Z-Velocity (BLUE) at " + str(maxVel)
##            elif velZ < minVel:
##                blue = velZ
##                minVel = velZ
##                print "Current Min Velocity is: Z-Velocity (BLUE) at " + str(minVel)
        elif radius:
            glClearColor(1.0,1.0,1.0,1.0)
            red = rad
            green = rad
            blue = rad
        elif greyScale:
            #glClearColor(1.0,1.0,1.0,1.0)
            glClearColor(0.0,0.0,0.0,1.0)
            red = rad
            green = rad
            blue = rad

        else:
            red = 0
            green = 0
            blue = 0

        glPushMatrix()
        glTranslate(p.x[i], p.y[i], p.z[i])
        glColor(red, green, blue, alpha)
        
        if teapot:
            glutSolidTeapot(p.r[i])
        if donut:
            glutSolidTorus(p.r[i]/2, p.r[i], SLICES, STACKS)
        if sphere:
            glutSolidSphere(p.r[i], SLICES, STACKS)
        glPopMatrix()
    glutSwapBuffers()


def idle():
    global COUNT

    for i in range(UPDATE_FRAMES):
       integrate(f,p) # Move the system forward in time
       COUNT = COUNT + 1 
       if mod(COUNT,ADD_PARTICLE_INTERVAL) == 0:
           # Syntax is addParticle(x,y,z,vx,vy,vz,radius)
           # Note y is into page.
           p.addParticle(.25*randn(),L,.25*randn(),0,0,0,.3*randn()+1.)
           f(p)  # Update forces
    glutPostRedisplay()
        
def keyboard(key, x, y):
    global rotateZ, teapot, sphere, donut, radius, velocity, translateZ, lightMover, alpha, greyScale

    if key =='a':
        alpha = .5 #Transparent
    if key == 'A':
        alpha = 1 #Opaque

    if key == 'w':
        greyScale = True
        velocity = False
        radius = False
        
    if key == 'V':
        radius = True
        velocity = False
        greyScale = False
    if key == 'v':
        velocity = True
        radius = False
        greyScale = False
    #Changes the particle visual:
    if key == 't':
        teapot = True
        sphere = False
        donut = False
    if key == 'd':
        teapot = False
        sphere = False
        donut = True
    if key == 's':
        teapot = False
        sphere = True
        donut = False

    #Light zooming:
    if key == 'l':
        lightMover += 1
        print 'Current Light Position: ( ' + str(lightMover) + ', ' + str(lightMover) + ', ' + str(lightMover) + ')'
    if key == 'L':
        lightMover -= 1
        print 'Current Light Position: ( ' + str(lightMover) + ', ' + str(lightMover) + ', ' + str(lightMover) + ')'
        
    #Zooming:
    if key == 'm':
        translateZ += .5
    if key == 'n':
        translateZ -= .5
    if key == 'Z' :
        rotateZ -= 5
        print 'rotate along Z-axis ' + str(rotateZ) + ' degrees'

    if key == 'z' :
        rotateZ += 5
        print 'rotating along Z-axis ' + str(rotateZ) + ' degrees' 

    #Toggle Perspective Mode:
    if key == 'p':
        isPerspectiveMode = 1
        print "in perspective mode now.\n"
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, 1, .5, 100) #gluPerspective(angle, aspect ratio, clipping planes)
#        gluLookAt(L, L, L, 0, 0, 0, 0.0,1.0,0.0) #viewing object from slightly above       
        glMatrixMode(GL_MODELVIEW)

    #Orthogonal Mode:
    if key == 'o':
        isPerspectiveMode = 0;
        print "out of perspective mode now.\n"
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-L*2, L*2, -L*2, L*2, -L*2, L*2)
#        gluLookAt(L*2, L*2, L*2, L/2, L/2, L/2, 0.0,1.0,0.0) #viewing object from slightly above       
        glMatrixMode(GL_MODELVIEW)
        
    if key == 'q':
        print "'q' was pressed"
        exit(0)
    #glutPostRedisplay()
    
def special(key, x, y):
    global rotateX, rotateY
    if key == GLUT_KEY_UP:
        rotateX += 5
        print 'rotating along X-axis ' + str(rotateX) + ' degrees'

    if key == GLUT_KEY_LEFT:
        rotateY += 5
        print 'rotating along Y-axis ' + str(rotateY) + ' degrees'

    if key == GLUT_KEY_RIGHT:
        rotateY -= 5
        print 'rotating along Y-axis ' + str(rotateY) + ' degree'



    if key == GLUT_KEY_DOWN:
        rotateX -= 5
        print 'rotating along X-axis ' + str(rotateX) + ' degrees'

    #glutPostRedisplay()
#### Reshape Call-back Function ####

def reshape(width, height):
      glViewport(0,0,width,height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      glOrtho(-L, L, -L, L, -L, L)
      glMatrixMode(GL_MODELVIEW)



#### Main Program ####


def go():
    init()

    # Start the simulation

    glutMainLoop()

go()
  
#def visible(vis):
   
##if __name__ == '__main__':
##
##    # Open a window
##
##    # Initialize
##    init()
##
##    # Hand off control to event loop
##    glutMainLoop()


