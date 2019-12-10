import sys
import ctypes

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

import pywavefront
from pywavefront import visualization

user32 = ctypes.windll.user32

altura = user32.GetSystemMetrics(1)
largura = user32.GetSystemMetrics(0)

centroTela = [largura // 2, altura // 2]
matrixVisao = []

yaw = 0.0 #angulo X da camera
pitch = 0.0 #angulo Y da camera
cX, cY, cZ = [0.0, 3.0, 3.0] #posicao da camera
strafeX, strafeZ = [0, 0] #deslocamento lateral

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

def refresh():
    global strafeX
    global strafeZ

    x = np.cos(yaw) * np.cos(pitch)
    y = np.sin(pitch)
    z = np.sin(yaw) * np.cos(pitch)
    
    strafeX = np.cos(yaw - np.pi/2)
    strafeZ = np.sin(yaw - np.pi/2)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(cX, cY, cZ, cX + x, cY + y, cZ + z, 0, 1, 0)

def movimentoMouse(x, y):
    global yaw
    global pitch
    
    limite = 1.5
    vel = 0.02
    
    dx = x - centroTela[0]
    dy = y - centroTela[1]
    
    if dx:
        yaw += dx * vel
        refresh()
    
    if dy:
        pitch -= dy * vel
        if pitch < (-limite):
            pitch = -limite
        if pitch > limite:
            pitch = limite
        refresh()

    glutWarpPointer(centroTela[0], centroTela[1])
    
    glutPostRedisplay()

def arrasteMouse(x, y):
    glutWarpPointer(centroTela[0], centroTela[1])

def moveZ(vel): #move pra frente ou pra tras
    global cX
    global cY
    global cZ
    
    x = np.cos(yaw) * np.cos(pitch)
    y = np.sin(pitch)
    z = np.sin(yaw) * np.cos(pitch)
    
    cX += vel * x
    cY += vel * y
    cZ += vel * z
    
    refresh()
    
def moveX(vel): #move pra esquerda ou direita
    global cX
    global cZ
    
    cX += vel * strafeX
    cZ += vel * strafeZ
    
    refresh()

def keyboard(key, x, y):

    if ord(key) == 27:#'esc'  
        glutDestroyWindow(id)
        sys.exit(0)
    
    vel = 0.2
    
    if ord(key) == 119:#'w'
        moveZ(vel)
    if ord(key) == 115:#'s'
        moveZ(-vel)
    if ord(key) == 97:#'a'
        moveX(vel)
    if ord(key) == 100:#'d'
        moveX(-vel)
    
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
glutMotionFunc(movimentoMouse)
glutKeyboardFunc(keyboard)

glutFullScreen()
glutMainLoop()