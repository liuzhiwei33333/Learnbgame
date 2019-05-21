'''OpenGL extension ARB.copy_image

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.copy_image to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension enables efficient image data transfer between image
	objects (i.e. textures and renderbuffers) without the need to bind
	the objects or otherwise configure the rendering pipeline.
	
	This is accomplised by adding a new entry-point CopyImageSubData,
	which takes a named source and destination.
	
	CopyImageSubData does not perform general-purpose conversions
	such as scaling, resizing, blending, color-space, or format 
	conversions. It should be considered to operate in a manner 
	similar to a CPU memcpy, but using the GPU for the copy.
	
	CopyImageSubData supports copies between images with different
	internal formats, if the formats are compatible for TextureViews.
	
	CopyImageSubData also supports copying between compressed and
	uncompressed images if the compressed block / uncompressed texel
	sizes are the same.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/ARB/copy_image.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.ARB.copy_image import *
from OpenGL.raw.GL.ARB.copy_image import _EXTENSION_NAME

def glInitCopyImageARB():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION