# -*- coding: utf-8 -*-
##############################################################################
#
#  Shaderutils - Copyright (c) 2011 Richard Petri
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
#  2. Altered source versions must be plainly marked as such, and must not
#     be misrepresented as being the original software.
#  
#  3. This notice may not be removed or altered from any source
#     distribution.
#
##############################################################################
from OpenGL.GL import *

def loadShader(filename, shadertype):
    '''
    Creates, loads and compiles a shader by filename.
    '''
    shader = None
    try:
        with open(filename) as f:
            shader = glCreateShader(shadertype)
            glShaderSource(shader, f.readlines())
            glCompileShader(shader)
            if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
                info = glGetShaderInfoLog(shader)
                raise Exception, "Unable to compile shader. Infolog:\n%s" % (info,)
            return shader
    except Exception as e:
        if shader != None:
            glDeleteShader(shader)
        raise

def createProgram(fnvert, fnfrag):
    '''
    Creates, loads, compiles and links a program using two shaderfiles.
    '''
    prog = None
    vertsh = None
    fragsh = None
    try:
        prog = glCreateProgram()
    
        vertsh = loadShader(fnvert, GL_VERTEX_SHADER)
        fragsh = loadShader(fnfrag, GL_FRAGMENT_SHADER)

        glAttachShader(prog, vertsh)
        glAttachShader(prog, fragsh)
        glLinkProgram(prog)
        
        if glGetProgramiv(prog, GL_LINK_STATUS) != GL_TRUE:
            info = glGetProgramInfoLog(prog)
            raise Exception, "Unable to link program. Info log:\n%s" % (info)
        
        # Cleanup (don't worry, delete will only flag for deletion, if shaders are attached!)
        glDeleteShader(vertsh)
        vertsh = None
        glDeleteShader(fragsh)
        fragsh = None
        
        return prog
    except Exception as e:
        if prog != None:
            glDeleteProgram(prog)
        if vertsh != None:
            glDeleteShader(vertsh)
        if fragsh != None:
            glDeleteShader(fragsh)
        raise
        
def getUniformLocations(prog, *names):
    '''
    Retrieves the locations for uniforms in a program.
    '''
    return [glGetUniformLocation(prog, name) for name in names]
        
def getAttributeLocations(prog, *names):
    '''
    Retrieves the locations for attributes in a program.
    '''
    return [glGetAttribLocation(prog, name) for name in names]
    