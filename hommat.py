# -*- coding: utf-8 -*-
##############################################################################
#
#  Hommat library - Copyright (c) 2011 Richard Petri
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
import numpy as np
from math import pi, cos, sin, tan

def identity():
    '''Create the identity matrix.'''
    return np.identity(4, dtype=np.float32)
    
def translation(old, dir):
    '''Multiplies the old matrix with a translation in dir.'''
    M = np.identity(4, dtype=np.float32)
    M[:3, 3] = dir[:3]
    return np.dot(old, M)
    
def rotation(old, angle, dir):
    '''Multiplies the old matrix with a rotation around angle.'''
    cosa = cos(angle * pi / 180)
    sina = sin(angle * pi / 180)
    cosa1 = 1 - cosa
    M = np.array([[dir[0]**2 * cosa1 + cosa             , dir[0] * dir[1] * cosa1 - dir[2]*sina, dir[0] * dir[2] * cosa1 + dir[1]*sina, 0],
                  [dir[1] * dir[0] * cosa1 + dir[2]*sina, dir[1]**2 * cosa1 + cosa             , dir[1] * dir[2] * cosa1 - dir[0]*sina, 0],
                  [dir[2] * dir[0] * cosa1 - dir[1]*sina, dir[2] * dir[1] * cosa1 + dir[0]*sina, dir[2]**2 * cosa1 + cosa             , 0],
                  [0,0,0,1]
                 ], dtype=np.float32)
    return np.dot(old, M)
          
def scale(old, axes):
    '''Multiplies the old matrix with a scaleing matrix.'''
    M = np.array([[axes[0], 0, 0, 0],
                  [0, axes[1], 0, 0],
                  [0, 0, axes[2], 0],
                  [0, 0, 0, 1]
                 ], dtype=np.float32)
    return np.dot(old, M)

def ortho(old, l, r, b, t, n, f):
    '''Multiplies the old matrix with a orthogonal projection.'''
    M = np.array([[2.0 / (r - l), 0, 0, -float(r + l) / (r - l)],
                  [0, 2.0 / (t - b), 0, -float(t + b) / (t - b)],
                  [0, 0, 2.0 / (f - n), -float(f + n) / (f - n)],
                  [0,0,0,1]
                 ], dtype=np.float32)
    return np.dot(old, M)
                    
def perspective(old, fovy, aspect, near, far):
    '''Multiplies the old matrix with a perspective projection.'''
    f = 1.0 / tan(fovy * pi / 360.0)
    M = np.array([[f / aspect, 0, 0, 0],
                  [0, f, 0, 0],
                  [0, 0, float(far + near) / (near - far), (2.0 * far * near) / (near - far)],
                  [0, 0, -1, 0]
                 ], dtype=np.float32)
    return np.dot(old, M)
                    
def lookat(old, eye, at, up = np.array([0,1,0,1])):
    '''Multiplies the old matrix with a lookat transformation.'''
    f = at[:3] - eye[:3]
    f *= 1 / np.linalg.norm(f)
    up /= np.linalg.norm(up[:3])
    s = np.cross(f, up[:3])
    u = np.cross(s, f)
    M = np.identity(4, dtype=np.float32)
    M[0, :3] = s
    M[1, :3] = u
    M[2, :3] = -f
    return np.dot(old, translation(M, -eye))

    