#!/usr/bin/env python

import sys
from setuptools import setup

if sys.version_info < (2, 7, 0) or (3,) < sys.version_info < (3, 2, 0):
    sys.stderr.write('ERROR: You need either Python2 2.7 or later '
                     'or Python3 3.2 or later '
                     'to install the typing package.\n')
    exit(1)

version = '0.0.1.dev1'
description = 'Type annotations for Python'
long_description = '''
Typing -- Type annotations for Python

Typing is intended as a standard notation for Python function and variable type
annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime
type checkers, static analyzers, IDEs and other tools. The typing module
originates from the mypy optional static type checker for Python.
'''.lstrip()

package_dir = {2: 'python2', 3: '.'}[sys.version_info.major]
classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development',
]

setup(name='typing',
      version=version,
      description=description,
      long_description=long_description,
      author='Jukka Lehtosalo',
      author_email='jukka.lehtosalo@iki.fi',
      url='http://www.mypy-lang.org/',
      license='MIT License',
      platforms=['POSIX'],
      package_dir={'': package_dir},
      py_modules=['typing'],
      classifiers=classifiers)
