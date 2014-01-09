# This script animates a bouncing ball using OpenGL.
# Written  by Glen Granzow on November 11, 2011.
# Modified by Glen Granzow on November 18, 2011.

from OpenGL.GL   import *
from OpenGL.GLUT import *

#### Reshape Call-back Function ####

def reshape(width, height):
  glViewport(0,0,width,height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  glOrtho(-1-radius,1+radius, 0-radius,2+radius, -1,1)
  glMatrixMode(GL_MODELVIEW)
  glLight(GL_LIGHT0, GL_POSITION, [0.7, 1.0, 2.0, 0.0]);

##### Idle Call-back Function ####

def idle():
# Update the ball's position and velocity (using Euler's method)
  global x, y, vx, vy, theta

  vy = vy - gravity
  x  = x + vx
  y  = y + vy

  if x < -1:
    x  = -2 - x
    vx = - vx * elasticity

  if x > 1:
    x  = 2 - x
    vx = -vx * elasticity

  if y < 0:
    y  = - y
    vy = - vy * elasticity

#  theta += 0.01
  
  glutPostRedisplay()

##### Keyboard Call-back Functions ####

def keyboard(key, x, y):
  global color, elasticity, gravity, theta, phi

  if key == 'c':
    color = not color
  if key == 'w':
    color = False
    glColor(1.0,1.0,1.0) # white

  if key == 'e':
    elasticity -= 0.1
    print "'e' was pressed: elasticity =", elasticity
  if key == 'E':
    elasticity += 0.1
    print "'E' was pressed: elasticity =", elasticity

  if key == 'g':
    gravity *= 2
    print "'g' was pressed: gravity =", gravity
  if key == 'G':
    gravity /= 2
    print "'G' was pressed: gravity =", gravity
    
  if key == 'r':
    theta += 1
  if key == 'R':
    phi += 1

  if key == 'q':
    print "'q' was pressed"
    exit(0)

def special(key, x, y):
  global vx, vy

  if key == GLUT_KEY_UP:
    vy += 100*gravity
    print 'UP    key was pressed: vy =', vy

  if key == GLUT_KEY_LEFT:
    vx -= 100*gravity
    print 'LEFT  key was pressed: vx =', vx

  if key == GLUT_KEY_RIGHT:
    vx += 100*gravity
    print 'RIGHT key was pressed: vx =', vx

##### Display Call-back Function ####

def display():
  if color:
    v = max(0.001,(vx*vx + vy*vy)**0.5)
    glColor(abs(vx)/v,1.0-abs(vy)/v,abs(vy)/v);
  else:
    glColor(1.0, 1.0, 1.0)

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glLoadIdentity()
  glTranslate(x,y,0)
  glRotate(theta, 0, 0, 1)
  glRotate(phi, 1, 0, 0)
  glutSolidSphere(radius, 20, 10)
  glColor(0.5, 0.5, 0.5)
  glutWireSphere(radius, 20, 10)
  glutSwapBuffers()

#### Main Program ####

# Ball parameters

color   = False
radius  = 0.2
x, y    = (0, 0)   # position
vx, vy  = (0, 0)   # velocity
gravity = 0.00001  # acceleration
elasticity = 1     # damping
theta, phi = 0, 0

# Initialization

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
glutInitWindowPosition(100,0)
glutInitWindowSize(500,500)
glutCreateWindow("Bouncing Ball")

# Register Call-back Functions

glutReshapeFunc(reshape)
glutIdleFunc(idle)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special)
glutDisplayFunc(display)

# Lighting Parameters

glEnable(GL_LIGHTING);
glEnable(GL_LIGHT0);
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_POLYGON_OFFSET_FILL)  # Prevents some hidden line problems when drawing
glPolygonOffset(1.0, 1.0);        # a wireframe on top of filled polygons.

glEnable(GL_DEPTH_TEST)

# Start the simulation

glutMainLoop()
