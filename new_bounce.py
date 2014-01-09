#! /usr/bin/env python
from particles import *
from particleInitialize import *
from utils import *

import sys
import time
import signal
import logging

class BouncingBall:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

        self.t0 = time.time()
        self.t_start = self.t0
        self.dt = 0.1 # time step taken by the time integration routine
        self.L = 10. # size of the box
        self.count = 1 # number of time steps computed
        self.update_frames = 2 # how often to redraw screen
        self.add_particle_interval = 10 # how often to add a new particle
        # how resolved are the spheres? (originally 25)
        self.stacks = 25
        self.slices = 25

        self.f = GranularMaterialForce()
        self.p = Particles(self.L, self.f, periodicY = 0)
        particleInitialize(self.p, 'one', self.L)
        self.integrate = VerletIntegrator(self.dt)

        signal.signal(signal.SIGINT, self.sigint)
        self.camera = {'angle': 0, 'x': 0, 'y': 0, 'z': 0}
        self.initialize_gl()


    def initialize_gl(self):
        glutInit(sys.argv)

        draw_window(GLUT_RGB | GLUT_DOUBLE, 'Bouncing Balls', size = (800, 800))

        # background color
        glClearColor(1, 1, 1, 1)

        # enables the depth-testing feature (depth buffer is the Z-axis)
        glEnable(GL_DEPTH_TEST)

        # Prevents some hidden line problems when drawing
        glEnable(GL_POLYGON_OFFSET_FILL)
        glEnable(GL_LIGHTING);
        glEnable(GL_LIGHT0);
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);

        # register callbacks
        glutIdleFunc(self.idle)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.keyboard)
        glutDisplayFunc(self.display)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(-self.L, self.L, -self.L, self.L, -self.L, self.L)

        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);


    def run(self):
        """Hand off control to the OpenGL event loop."""
        glutMainLoop()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # glRotate(self.camera['angle'] % 90,q self.camera['x'] % 100, self.camera['y'], self.camera['z'])

        # manipulate the model matrix from here on out
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotate(self.camera['x'], 1, 0, 0)
        glRotate(self.camera['y'], 0, 1, 0)
        glRotate(self.camera['z'], 0, 0, 1)



        # no idea
        glEnable(GL_CULL_FACE)
        glEnable(GL_POLYGON_SMOOTH)
        glCullFace(GL_BACK)

        h = lambda x: float(x) / 255.0

        alpha = 0.5
        # glutWireTeapot(5)
        for i in range(self.p.N):
            # glLoadIdentity()
            glPushMatrix()
            glTranslate(self.p.x[i], self.p.y[i], self.p.z[i])

            glColor(0.7, 1.0, 0.3, alpha)
            glutSolidSphere(self.p.r[i], self.slices, self.stacks)
            glPopMatrix()

        # swap the drawn buffer from the background with the foreground buffer
        glutSwapBuffers()

    def reshape(self):
        """Callback for resizing the window."""
        pass

    def idle(self):
        """Idle callback function for OpenGL."""
        for i in range(self.update_frames):
            self.integrate(self.f, self.p) # Move the system forward in time
            self.count += 1
            if mod(self.count, self.add_particle_interval) == 0:
                # Syntax is addParticle(x,y,z,vx,vy,vz,radius)
                # Note y is into page.
                self.p.addParticle(.25*randn(), self.L, .25*randn(), 0, 0, 0, .3*randn()+1.)
                self.f(self.p)  # Update forces
        glutPostRedisplay()

    def keyboard(self, key, x, y):
        """Keyboard mapping callback."""
        self.logger.debug("key = %s\tx = %d\ty = %d" % (key, x, y))

        print self.camera
        if key in ['q', 'Q', '']:
            self.quit()
        elif key == GLUT_KEY_UP:
            self.camera['z'] += 15
        elif key == GLUT_KEY_RIGHT:
            self.camera['x'] += 15
        elif key == GLUT_KEY_DOWN:
            self.camera['z'] -= 15
        elif key == GLUT_KEY_LEFT:
            self.camera['x'] -= 15
        elif key == 'r':
            self.camera['angle'] += 15
        elif key == 'R':
            self.camera['angle'] -= 15
        else:
            self.logger.debug('...not recognized')
            return

        glutPostRedisplay()

    def sigint(self, signum, frame):
        """Respond to SIGINT (Ctrl-C)"""
        quit()

    def quit(self):
        self.logger.debug("Quitting...");
        sys.exit(0)

if __name__ == '__main__':
    b = BouncingBall()
    b.run()



