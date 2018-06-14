import os
import sys
from setuptools import setup, find_packages
from setuptools.command.egg_info import manifest_maker

if sys.version_info[:2] < (3, 6):
    print("Python >= 3.6 is required.")
    sys.exit(-1)

requires = ['notebook>=5.5.0']


def about(package):
    ret = {}
    filename = os.path.join(os.path.dirname(__file__), package, '__about__.py')
    with open(filename, 'rb') as file:
        exec(compile(file.read(), filename, 'exec'), ret)
    return ret


def read(filename):
    if not os.path.exists(filename):
        return ''

    with open(filename) as f:
        return f.read()


info = about('nbkickoff')
manifest_maker.template = 'setup.manifest'

setup(
    name=info['__title__'],
    version=info['__version__'],
    description=info['__summary__'],
    long_description=read('README.md'),
    url=info['__url__'],
    license=info['__license__'],

    author=info['__author__'],
    author_email=info['__email__'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Jupyter',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ],

    packages=find_packages(exclude=['test*']),
    install_requires=requires,
)