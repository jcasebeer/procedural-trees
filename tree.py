import pygame
import math
import random as RAND
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# useful constants
PI = math.pi
# coefficient for Degrees to Radian
PID = PI/180.0

def normalize(x,y,z):
    m = (x*x+y*y+z*z)**0.5
    return x/m, y/m, z/m

def random(num):
    return RAND.random()*num

def degtorad(deg):
    return deg*PID

# syntatic sugar for getting the horizontal component
# of a rotation
def lengthdir_x(len,dir):
    return len*math.cos(degtorad(dir))

def lengthdir_y(len,dir):
    return len*math.sin(degtorad(dir))

# where the magic happens
def gen_branch(size,x,y,z,xto,yto,zto):
    # minimum branch width
    if size>=4.0:
        # draw the branch with a line
        glBegin(GL_LINES)
        glVertex3f(x,y,z)
        glVertex3f(xto,yto,zto)
        glEnd()

        # make 2 to 4 other branches
        for i in range(2+int(random(3))):
            # get the direction of the previous branch
            xdir = xto - x
            ydir = yto - y
            zdir = zto - z

            # normalize the direction
            xdir, ydir, zdir = normalize(xdir,ydir,zdir)

            # offset the direction by some amount
            xdir+=random(1.4)-0.7
            ydir+=random(1.4)-0.7
            zdir+=random(1.4)-0.7

            # normalize the direction again!
            xdir, ydir, zdir = normalize(xdir, ydir, zdir)

            # run the branch function again with the new vectors
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

# helper function for the recursive gen_branch
def gen_tree(size):
    gen_branch(size,0,0,0,0,0,size)

# used to move x,y coordinates in a direction,
# in degrees, by a speed.
def moveDir(dir,speed,x,y):
    xChange = lengthdir_x(1,dir)
    yChange = lengthdir_y(1,dir)
    x+=xChange
    y+=yChange
    return (x,y)

def main():
    # set up pygame/opengl stuff
    display = (800,600)
    aspect = float(display[0])/display[1]

    # camera variables
    x = -256
    y = 0.0
    z = 0.0
    view_height = 16.
    hdir = 0.0
    vdir = 30.
    speed = 4.

    # start pygame w/ opengl enabled
    pygame.display.init()
    pygame.display.set_mode(display,DOUBLEBUF|OPENGL)

    # generate a tree and stick it in a display list
    # for speed
    model_tree = glGenLists(1)
    glNewList(model_tree,GL_COMPILE)
    gen_tree(64)
    glEndList()

    # main loop
    while 1:

        # exiting stuff
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

        # control the camera, wasd for strafing on the 
        # x,y plane and arrow keys for camera control
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

        # clamp vertical direction of camera
        if vdir<-89: vdir = -89
        if vdir>89: vdir = 89

        # opengl stuff
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.25,0.0625,0.125,1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # set camera apeture, aspect ratio, clipping planes
        gluPerspective(90,aspect,0.1,32000.0)

        # point the camera, z+ is the up vector
        gluLookAt(
            x,
            y,
            z+view_height,
            x+lengthdir_x(lengthdir_x(1,vdir),hdir),
            y+lengthdir_y(lengthdir_x(1,vdir),hdir),
            z+view_height+lengthdir_y(1,vdir),
            0.,0.,1.
        )
        # draw our tree
        glCallList(model_tree)
        glPopMatrix()

        # refresh the window and limit framerate
        pygame.display.flip()
        pygame.time.delay(16)

    # clear the tree display list when we're done with it
    glDeleteLists(model_tree,1)

# loop so that you can press enter to restart app/get new trees
again = True
while(again):
    again = main()
