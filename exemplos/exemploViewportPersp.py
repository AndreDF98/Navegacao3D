import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
    
def init():

    m = glGetFloatv(GL_PROJECTION_MATRIX)
    glClearColor(0.0, 0.0, 0.7, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [-20.,2.,-2.,1.]
    lightZeroColor = [1.8,1.0,0.8,1.0] #green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glutDisplayFunc(display)
    glMatrixMode(GL_PROJECTION)
    #gluPerspective(GLdouble fovy,  GLdouble aspect,  GLdouble zNear,  GLdouble zFar);
    #glLoadIdentity()
    gluPerspective(40.,1.,1.,40.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,10,
              0,0,0,
              0,1,0)
    glPushMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    color = [1.0,0.,0.,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    glutSolidTeapot(1)
    glutSwapBuffers()
    glColor3f(1.0, 0.0, 0.0) 
    glFlush ()
    
def keyboard(key, x, y):
  global wid
  global hei

  if ord(key) == 49:#'1'  
    glLoadIdentity();
    gluLookAt(0,0,10,
              0,0,0,
              0,1,0)
    
    glutPostRedisplay()
  if ord(key) == 50:#'2'  
    glLoadIdentity();
    gluLookAt(0,0,20,
              0,0,0,
              0,1,0) 
    glutPostRedisplay()
  if ord(key) == 51:#'3'  
    glRotatef(-15.0,1.0,0.0,0.0)
    glutPostRedisplay()  
  if ord(key) == 52:#'4'  
    glRotatef(-15.0,0.0,1.0,0.0)
    glutPostRedisplay()    
  if ord(key) == 53:#'5'  
    glRotatef(-15.0,0.0,0.0,1.0)
    glutPostRedisplay()    
  if ord(key) == 54:#'6'  
    glTranslatef(0.0,0.0,0.1)
    glutPostRedisplay()    
  if ord(key) == 55:#'7'  
    glTranslatef(0.0,0.0,-0.1)
    glutPostRedisplay()    
  
    
  return
    
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(600, 600)
glutInitWindowPosition(100, 100)
glutCreateWindow('Perspective')
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()