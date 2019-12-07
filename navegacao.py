import sys
import ctypes

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pywavefront
from pywavefront import visualization

user32 = ctypes.windll.user32

altura = user32.GetSystemMetrics(1)
largura = user32.GetSystemMetrics(0)

centroTela = [largura // 2, altura // 2]
matrixVisao = []

#objeto = pywavefront.Wavefront('objetos/extintor.obj')
#objeto = pywavefront.Wavefront('objetos/cadeira.obj')
objeto = pywavefront.Wavefront('objetos/laboratorio.obj')

def init():
    global matrixVisao
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glColorMaterial(GL_BACK, GL_DIFFUSE)
    glEnable(GL_COLOR_MATERIAL)
    glClearColor(0.1, 0.1, 0.1, 0.0)
    glutSetCursor(GLUT_CURSOR_DESTROY)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (largura/altura), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, 3, 3, 0, 0, 0, 0, 1, 0)
    matrixVisao = glGetFloatv(GL_MODELVIEW_MATRIX)
    #perspectiveView
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    visualization.draw(objeto)
    
    glutSwapBuffers()
    glFlush ()

def reshape(l, a):
    global altura
    global largura
    altura = a
    largura = l
    
def cliqueMouse(botao, estado, x, y):
    return

def movimentoMouse(x, y):
    global matrixVisao

    glutWarpPointer(centroTela[0], centroTela[1])
    
    glLoadIdentity()
    glPushMatrix()
    glLoadIdentity()
    
    #baixo
    if y > centroTela[1]:
        #pass
        glRotatef(0.5, 1.0, 0.0, 0.0)
    #cima
    if y < centroTela[1]:
        #pass
        glRotatef(-0.5, 1.0, 0.0, 0.0)
    
    #direita
    if x > centroTela[0]:
        #pass
        glRotatef(0.5, 0.0, 1.0, 0.0)
    #esquerda
    if x < centroTela[0]:
        #pass
        glRotatef(-0.5, 0.0, 1.0, 0.0)
        
    glMultMatrixf(matrixVisao)
    matrixVisao = glGetFloatv(GL_MODELVIEW_MATRIX)

    glPopMatrix()
    glMultMatrixf(matrixVisao)
    
    glutPostRedisplay()

def arrasteMouse(x, y):
    glutWarpPointer(centroTela[0], centroTela[1])

def keyboard(key, x, y):
    global matrixVisao
    
    glLoadIdentity()
    glPushMatrix()
    glLoadIdentity()

    if ord(key) == 27:#'esc'  
        glutDestroyWindow(id)
        sys.exit(0)
    
    if ord(key) == 119:#'w'
        glTranslatef(0,0,0.2)
    if ord(key) == 115:#'s'
        glTranslatef(0,0,-0.2)
    if ord(key) == 100:#'d'
        glTranslatef(-0.2,0,0)
    if ord(key) == 97:#'a'
        glTranslatef(0.2,0,0)
        
    glMultMatrixf(matrixVisao)
    matrixVisao = glGetFloatv(GL_MODELVIEW_MATRIX)

    glPopMatrix()
    glMultMatrixf(matrixVisao)
    
    glutPostRedisplay()

glutInit(sys.argv) 
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(largura, altura)
id = glutCreateWindow('Navegacao')
init()

glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(cliqueMouse)
glutPassiveMotionFunc(movimentoMouse)
glutMotionFunc(arrasteMouse)
glutKeyboardFunc(keyboard)

glutFullScreen()
glutMainLoop()