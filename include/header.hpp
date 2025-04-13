#pragma once

#define GL_GLEXT_PROTOTYPES
#define GLX_GLXEXT_PROTOTYPES

#include <dlfcn.h>
#include <cstring>
#include <iostream>
#include <stdio.h>

#include <GL/gl.h>
#include <EGL/egl.h>
#include <GL/glx.h>

#include "dlsym.hpp"

#define PUBLIC __attribute__((visibility("default")))
#define PRIVATE __attribute__((visibility("hidden")))
#define INITIALIZER __attribute__((constructor))
