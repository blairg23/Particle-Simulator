# This script animates a bouncing beach ball using OpenGL.
# Written by Glen Granzow on November 18, 2011.

from OpenGL.GL   import *
from OpenGL.GLU  import *
from OpenGL.GLUT import *

#################################
#### Idle Call-back Function ####
#################################

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
    
  theta -= vx/radius * 180/3.141592654

  glutPostRedisplay()

######################################
#### Keyboard Call-back Functions ####
######################################

def keyboard(key, x, y):
  global elasticity, gravity, theta, phi, stripes, sandColor

  if key == 'e':
    elasticity -= 0.1
  if key == 'E':
    elasticity += 0.1

  if key == 'g':
    gravity *= 2
  if key == 'G':
    gravity /= 2

  if key == 'r':
    theta += 1
  if key == 'R':
    phi += 1

  if key == 'c':
    if stripes[0][1] == 255:
      stripes = [[255,  0,  0],[255,255,  0],[0,255,  0],[0,  0,  0],
                 [255,255,255],[  0,255,255],[0,  0,255],[255,0,255]]
    else:
      stripes = [[255,255,255],[255,0,0],[255,255,255],[255,0,0],
                 [255,255,255],[255,0,0],[255,255,255],[255,0,0]]
    key = 'S'
  
  if key == 's':
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1, 8, 0, GL_RGB, GL_UNSIGNED_BYTE, stripes)
  if key == 'S':
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 8, 1, 0, GL_RGB, GL_UNSIGNED_BYTE, stripes)

  if key == ' ':
    if sandColor[0] == 0.9:
      sandColor = (0.75, 0.75, 0.5)
      glClearColor(0.25, 0.25, 0.75, 0.0)
    else:
      sandColor = (0.9, 0.9, 0.7)
      glClearColor(0.6, 0.8, 1.0, 0.0)

  if key == 'q':
    exit(0)

def special(key, x, y):
  global vx, vy

  if key == GLUT_KEY_UP:
    vy += (3.6*gravity)**0.5

  if key == GLUT_KEY_LEFT:
    vx -= (0.1*gravity)**0.5

  if key == GLUT_KEY_RIGHT:
    vx += (0.1*gravity)**0.5

####################################
#### Display Call-back Function ####
####################################

def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  glLoadIdentity()
  glDisable(GL_TEXTURE_2D);
  glColor(sandColor)
  glRectf(-2.0, -1.0, 2.0, 0.15)

  glTranslate(x, y, 0)
  glRotate(theta, 0, 0, 1)
  glRotate(phi, 1, 0, 0)
  glEnable(GL_TEXTURE_2D);
  gluSphere(beachBall, radius, 20, 10)

  glutSwapBuffers()

######################
#### Main Program ####
######################

# Ball parameters

radius  = 0.2
x, y    = (   0.4, 0)     # position
vx, vy  = (-0.001, 0.006) # velocity
gravity = 0.00001         # acceleration
elasticity = 0.9          # damping
theta, phi = (20.0, 45.0) # rotational position

# Initialization

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
glutInitWindowPosition(100,100)
glutInitWindowSize(500,500)
glutCreateWindow("Beach Ball")

glEnable(GL_DEPTH_TEST)
glClearColor(0.6, 0.8, 1.0, 0.0)  # Color of the sky
sandColor = (0.9, 0.9, 0.7)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-1-radius,1+radius, 0-1.5*radius,2+0.5*radius, -1,1)
glMatrixMode(GL_MODELVIEW)

# Register Call-back Functions

glutIdleFunc(idle)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special)
glutDisplayFunc(display)

# Use texture mapping to "paint" the ball

stripes = [[255,255,255],[255,0,0],[255,255,255],[255,0,0],
           [255,255,255],[255,0,0],[255,255,255],[255,0,0]]
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 8, 1, 0, GL_RGB, GL_UNSIGNED_BYTE, stripes)

beachBall = gluNewQuadric()
gluQuadricTexture(beachBall, GL_TRUE);

# Start the simulation

glutMainLoop()
