Richards OpenGL 3.2 Core Profile Example
========================================

This is a simple example to show how to access the OpenGL 3.2 Core Profile in
Mac OS X Lion (or any other OS with support for it) using Python, [PyOpenGL][1],
[Numpy][2], and the [GLFW][3] Library. GLFW serves as a GLUT replacement, since GLUT
doesn't support the GL Context creation for the Core Profile on Mac OS X Lion.
Note that a PyOpenGL Version > 3.0.2 is required for this to work (smaller
versions seem to have a bug when using the VAO extension). The missing matrix
functionallity of OpenGL (< 3.0) is replaced by a tiny library i've written for
this example (see `hommat.py`).

The GLFW bindings for Python were written by Nicolas P. [Rougier][4], but i
modified them a tiny bit (see `glfw.py`). The bindings are written using the
python ctypes functionallity and should run with any python distribution on any
platform that supports ctypes (i've only tested OSX and Linux). The bindings
will look for a binary of GLFW (libglfw.so/.dylib/.dll) in the usual places. You
can provide a specific binary by placing the path into GLFW_LIBRARY Environment
variable.

[1]: http://pyopengl.sourceforge.net/
[2]: http://numpy.scipy.org/
[3]: http://www.glfw.org
[4]: http://www.loria.fr/~rougier/coding/python.html
    