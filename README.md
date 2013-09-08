modloader.py
============

Provides functionality to load a bunch of python modules matching a certain criteria at runtime.
It basically acts as a simple plugin mechanism. It allows you to drop python files with a
particular signature (currently: a specified method) into a directory and import all of those
files at runtime.
