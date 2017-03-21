from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from distutils.extension import Extension

ext = Extension('analysis_cython',
                sources=["analysis_cython.pyx"],
                compiler_directives={'boundscheck':False,
                    'wraparound':False,
                    'nonecheck':False})

setup(
    ext_modules = cythonize(ext)
)
