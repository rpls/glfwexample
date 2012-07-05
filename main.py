#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
##############################################################################
#
#  OpenGL 3.2 Core Profile Example - Copyright (c) 2011 Richard Petri
#  
#  This software is provided 'as-is', without any express or implied
#  warranty. In no event will the authors be held liable for any damages
#  arising from the use of this software.
#  
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
#  
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would
#     be appreciated but is not required.
#
##############################################################################
import os
import sys
import ctypes
import numpy as np
import shaderutil
import hommat as hm
import time
# A * import gives the code a familiar C-Ish feeling. Since all the functions are prefixed with gl/glfw, it's not too bad.
from glfw import *
from OpenGL.arrays.vbo import VBO
from OpenGL.GL.ARB.vertex_array_object import *

# A triangle strip for a cube. Layout is 4xPosition, 4xColor
cubedata = np.array([-1,-1, 1, 1, 0, 0, 0, 0, #1
                      1,-1, 1, 1, 1, 0, 0, 0, #2
                      1, 1, 1, 1, 1, 1, 0, 0, #3
                      1,-1,-1, 1, 1, 0, 1, 0, #4
                      1, 1,-1, 1, 1, 1, 1, 0, #5
                     -1, 1,-1, 1, 0, 1, 1, 0, #6
                      1, 1, 1, 1, 1, 1, 0, 0, #7
                     -1, 1, 1, 1, 0, 1, 0, 0, #8
                     -1,-1, 1, 1, 0, 0, 0, 0, #9
                     -1, 1,-1, 1, 0, 1, 1, 0, #10
                     -1,-1,-1, 1, 0, 0, 1, 0, #11
                      1,-1,-1, 1, 1, 0, 1, 0, #12
                     -1,-1, 1, 1, 0, 0, 0, 0, #13
                      1,-1, 1, 1, 1, 0, 0, 0, #14
                    ], dtype = np.float32)
                    
campos = np.array([2.5, 1.5, 2.5, 1], dtype = np.float32)
center = np.array([0.0,0.0,0.0,1.0], dtype = np.float32)

modelview_mat = hm.lookat(hm.identity(), campos, center)
perspective_mat = None
mvp = None

def resizeWindow(width, height):
    global mvp, modelview_mat, perspective_mat
    glViewport(0, 0, width, height)
    perspective_mat = hm.perspective(hm.identity(), 70, float(width) / height, 0.1, 10.0)
    mvp = np.dot(perspective_mat, modelview_mat)

running = True

# A light example for a key callback.
def keypress(key, action):
    if key == GLFW_KEY_ESC:
        global running
        running = False
    
if __name__ == "__main__":
    # Something in glfwInit changes the cwd.
    cwd = os.getcwd()
    # Initialize
    if not glfwInit():
        print >> sys.stderr, "Unable to initialize GLFW."
        sys.exit(-1)
    # Restore the old cwd.
    os.chdir(cwd)
    # Set Window hints for OpenGL 3.2 Core profile.
    glfwOpenWindowHint(GLFW_OPENGL_VERSION_MAJOR, 3)
    glfwOpenWindowHint(GLFW_OPENGL_VERSION_MINOR, 2)
    glfwOpenWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
    glfwOpenWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)    
    if not glfwOpenWindow(400, 300, 0, 0, 0, 0, 32, 0, GLFW_WINDOW):
        print >> sys.stderr, "Unable to open Window."
        glfwTerminate()
        sys.exit(-1)
    glfwSetWindowSizeCallback(resizeWindow)
    glfwSetKeyCallback(keypress)
    glfwSetWindowTitle("OpenGL Core Profile Test")
    glfwEnable(GLFW_AUTO_POLL_EVENTS) # Enables the polling for key/mouse events in the swap buffer function!
    resizeWindow(400, 300)
    # Print some OpenGL information.
    print "OpenGL Information:"
    for prop in ["GL_VENDOR", "GL_RENDERER", "GL_VERSION", "GL_SHADING_LANGUAGE_VERSION"]:
        print "\t%s = %s" % (prop, glGetString(locals()[prop]))

    # Set up OpenGL Stuff.
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glClearColor(1, 1, 1, 0)
    glPointSize(5)
    # Set up the shader.
    prog = shaderutil.createProgram("./shader.vs", "./shader.fs")
    mvploc = glGetUniformLocation(prog, "mvp")
    positionloc = glGetAttribLocation(prog, "vs_position")
    colorloc = glGetAttribLocation(prog, "vs_color")    
    
    # Setup VAO
    vertobj = glGenVertexArrays(1)
    glBindVertexArray(vertobj)
    # Setup the VBO (using the fancy VBO Object from pyopengl, doing it "manually" would also be a possibility)
    vertbuf = VBO(cubedata, GL_STATIC_DRAW)
    vertbuf.bind()
    glEnableVertexAttribArray(positionloc)
    glEnableVertexAttribArray(colorloc)
    glVertexAttribPointer(positionloc, 4, GL_FLOAT, GL_TRUE, 8 * 4, vertbuf+0) # "+0" since we need to create an offset.
    glVertexAttribPointer(colorloc, 4, GL_FLOAT, GL_TRUE, 8 * 4, vertbuf+16) # 4 * 4 Bytes per float.
    vertbuf.unbind() # We can unbind the VBO, since it's linked to the VAO
    # glBindVertexArray(0)
    
    running = True
    t = time.time()
    rotation = 0.0
    while running:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(prog)
        glUniformMatrix4fv(mvploc, 1, GL_TRUE, hm.rotation(mvp, rotation,[0,1,0]).tolist())
        # glBindVertexArray(vertobj)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 14)
        glDrawArrays(GL_POINTS, 0, 14)
        glfwSwapBuffers()
        # glfwPollEvents() # This would poll for key/mouse events manually.
        # Do the rotation thing...
        rotation += (time.time() - t) / 5 * 360
        t = time.time()
        # Stop running if window gets closed.
        running = running and glfwGetWindowParam(GLFW_OPENED)
        
    glfwTerminate()