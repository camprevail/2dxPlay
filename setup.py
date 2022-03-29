import os
from distutils.core import setup
import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='2dxPlay',
    version='1.0.0',
    packages=['twodxPlay'],
    entry_points='''
        [console_scripts]
        2dxplay=twodxPlay.main:main
    ''',
    keywords=['2dx'],
    url='https://github.com/camprevail/2dxPlay',
    license='MIT',
    author='camprevail',
    author_email='cam.anderson573@gmail.com',
    description='Play a .2dx file.',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pygame", "setuptools"],
)
