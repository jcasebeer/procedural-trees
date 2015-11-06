import pygame
import math
import random as RAND
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

PI = math.pi
PID = PI/180.0

def normalize(x,y,z):
    m = (x*x+y*y+z*z)**0.5
    return x/m, y/m, z/m

def random(num):
    return RAND.random()*num

def degtorad(deg):
    return deg*PID

def lengthdir_x(len,dir):
    return len*math.cos(degtorad(dir))

def lengthdir_y(len,dir):
    return len*math.sin(degtorad(dir))

def gen_branch(size,x,y,z,xto,yto,zto):
    if size>=4.0:
        glBegin(GL_LINES)
        glVertex3f(x,y,z)
        glVertex3f(xto,yto,zto)
        glEnd()

        for i in range(2+int(random(3))):
            xdir = xto - x
            ydir = yto - y
            zdir = zto - z

            xdir, ydir, zdir = normalize(xdir,ydir,zdir)
            xdir+=random(1.4)-0.7
            ydir+=random(1.4)-0.7
            zdir+=random(1.4)-0.7
            xdir, ydir, zdir = normalize(xdir, ydir, zdir)

            gen_branch(
                size/(1+random(1.1)),
                xto,
                yto,
                zto,
                xto+xdir*size,
                yto+ydir*size,
                zto+zdir*size
            )
    else:
        return

def moveDir(dir,speed,x,y):
    xChange = lengthdir_x(1,dir)
    yChange = lengthdir_y(1,dir)
    x+=xChange
    y+=yChange
    return (x,y)

def gen_tree(size):
    gen_branch(size,0,0,0,0,0,size)

def main():
    display = (800,600)
    aspect = float(display[0])/display[1]

    x = -256
    y = 0.0
    z = 0.0
    view_height = 16.
    hdir = 0.0
    vdir = 30.
    speed = 4.

    pygame.init()
    pygame.display.set_mode(display,DOUBLEBUF|OPENGL)

    model_tree = glGenLists(1)
    glNewList(model_tree,GL_COMPILE)
    gen_tree(64)
    glEndList()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type ==pygame.KEYDOWN:
                if event.key == K_RETURN:
                    return True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            hdir+=2
        if keys[K_RIGHT]:
            hdir-=2
        if keys[K_UP]:
            vdir+=2
        if keys[K_DOWN]:
            vdir-=2
        if keys[K_w]:
            x,y = moveDir(hdir,speed,x,y)
        if keys[K_a]:
            x,y = moveDir(hdir+90,speed,x,y)
        if keys[K_s]:
            x,y = moveDir(hdir+180,speed,x,y)
        if keys[K_d]:
            x,y = moveDir(hdir-90,speed,x,y)

        if vdir<-89: vdir = -89
        if vdir>89: vdir = 89

        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_LINE_SMOOTH)
        #glLineWidth(1.0)
        glClearColor(0.25,0.0625,0.125,1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        gluPerspective(90,aspect,0.1,32000.0)
        gluLookAt(
            x,
            y,
            z+view_height,
            x+lengthdir_x(lengthdir_x(1,vdir),hdir),
            y+lengthdir_y(lengthdir_x(1,vdir),hdir),
            z+view_height+lengthdir_y(1,vdir),
            0.,0.,1.
        )
        glCallList(model_tree)
        glPopMatrix()
        pygame.display.flip()
        pygame.time.delay(16)

    glDeleteLists(model_tree,1)

again = True
while(again):
    again = main()
