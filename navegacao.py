import sys
import ctypes

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import time

import pywavefront
from pywavefront import visualization

user32 = ctypes.windll.user32

altura = user32.GetSystemMetrics(1)
largura = user32.GetSystemMetrics(0)

centroTela = [largura // 2, altura // 2]
matrixVisao = []

velocidade = 0.1 #Velocidade de movimentacao

yaw = 4.7 #angulo X da camera
pitch = -0.5 #angulo Y da camera
cX, cY, cZ = [-0.75, 2.0, 2.0] #posicao da camera
strafeX, strafeZ = [0, 0] #deslocamento lateral

demonstratemode = False #Modo de mover camera automaticamente entorno do objeto

#objeto = pywavefront.Wavefront('objetos/extintor.obj')
#objeto = pywavefront.Wavefront('objetos/cadeira.obj')
objeto = pywavefront.Wavefront('objetos/laboratorio.obj')

def init():
    global matrixVisao
    global strafeX
    global strafeZ
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glColorMaterial(GL_BACK, GL_DIFFUSE)
    glEnable(GL_COLOR_MATERIAL)
    glClearColor(0.1, 0.1, 0.1, 0.0)
    glutSetCursor(GLUT_CURSOR_NONE)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(70, (largura/altura), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    matrixVisao = glGetFloatv(GL_MODELVIEW_MATRIX)
    #perspectiveView
    glLoadIdentity()
    x = np.cos(yaw) * np.cos(pitch)
    y = np.sin(pitch)
    z = np.sin(yaw) * np.cos(pitch)
    gluLookAt(cX, cY, cZ, cX + x, cY + y, cZ + z, 0, 1, 0)
    
def demonstrate():
    global yaw
    global cX
    global cZ
    cX += 0.03 * strafeX
    cZ += 0.03 * strafeZ
    yaw+=0.0075
    time.sleep(0.01)
    refresh()
    
def display():
    glFlush()
    if demonstratemode:
        demonstrate()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    visualization.draw(objeto)
    glutSwapBuffers()
    glFlush()

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


def movimentoMouse1(x,y):
    pass
    
def movimentoMouse(x, y):
    global demonstratemode
    global yaw
    global pitch
    
    if not demonstratemode:
        limite = 1.5
        vel = 0.01
        
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

def moveY(up): #move pra esquerda ou direita
    global cY
    
    if up:
        glTranslatef(0,0.12,0)
        cY -= 0.12
    else:
        glTranslatef(0,-0.12,0)
        cY += 0.12
    refresh()

def keyboard(key, x, y):
    global stop
    global demonstratemode
    global yaw
    global pitch
    global strafeX, strafeZ, cX, cY, cZ
    global velocidade
    
    if ord(key) == 27:#'esc'  
        glutDestroyWindow(id)
        sys.exit(0)
        
    if ord(key) == 112:#p: Ativa/Destiva o modo de demonstacao
    
        if (demonstratemode == False): #Posiciona a camera na posicao inicial
            yaw = 4.7
            pitch = 0.0
            cX, cY, cZ = [-0.75, 2.0, 3.1]
            strafeX, strafeZ = [0, 0]
        demonstratemode = not demonstratemode #Liga/desliga modo de demonstacao

    if demonstratemode:
        return
    print(ord(key))
    if ord(key) == 119:#'w'
        moveZ(velocidade)
    elif ord(key) == 23:#Ctrl + w
        moveZ(velocidade*0.5)
    elif ord(key) == 87:#W
        moveZ(velocidade*1.5)
    elif ord(key) == 115:#'s'
        moveZ(-velocidade)
    elif ord(key) == 19:#Ctrl + s
        moveZ(-velocidade*0.5)
    elif ord(key) == 83:#S
        moveZ(-velocidade*1.5)
    elif ord(key) == 97:#'a'
        moveX(velocidade)
    elif ord(key) == 1:#Ctrl + a
        moveX(velocidade*0.5)
    elif ord(key) == 65:#A
        moveX(velocidade*1.5)
    elif ord(key) == 100:#'d'
        moveX(-velocidade)
    elif ord(key) == 4:#Ctrl + d
        moveX(-velocidade*0.5)
    elif ord(key) == 68:#D
        moveX(-velocidade*1.5)
    elif ord(key) == 102:#f Sobe
        moveY(True)
    elif ord(key) == 114:#r Desce
        moveY(False)
            
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
glutKeyboardFunc(keyboard)

glutFullScreen()
glutMainLoop()