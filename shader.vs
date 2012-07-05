#version 150

uniform mat4 mvp;

in vec4 vs_position;
in vec4 vs_color;
out vec4 fs_color;

void main() {
  fs_color = vs_color;
  gl_Position = mvp * vs_position;
}