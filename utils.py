"""Miscellaneous OpenGL utilities."""

from OpenGL.GL   import *
from OpenGL.GLU  import *
from OpenGL.GLUT import *

def draw_window(display_mode, title, size = (500, 500), pos = (0, 0)):
    """Initializes and draws a window."""
    glutInitWindowSize(size[0], size[1])
    glutInitWindowPosition(pos[0], pos[1])
    glutInitDisplayMode(display_mode)
    glutCreateWindow(title) # this is the only required call
