# -*- coding: utf-8 -*-
##############################################################################
# 
#  Shaderutilities
#  Authors:
#   - Richard Petri <dasricht at gmail.com>
#
#  This is free and unencumbered software released into the public domain.
#  
#  Anyone is free to copy, modify, publish, use, compile, sell, or
#  distribute this software, either in source code form or as a compiled
#  binary, for any purpose, commercial or non-commercial, and by any
#  means.
#  
#  In jurisdictions that recognize copyright laws, the author or authors
#  of this software dedicate any and all copyright interest in the
#  software to the public domain. We make this dedication for the benefit
#  of the public at large and to the detriment of our heirs and
#  successors. We intend this dedication to be an overt act of
#  relinquishment in perpetuity of all present and future rights to this
#  software under copyright law.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.
#   
#  For more information, please refer to <http://unlicense.org/>
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
    