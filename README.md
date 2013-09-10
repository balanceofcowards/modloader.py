modloader.py
============

Description
-----------

Provides functionality to load a bunch of python modules matching a certain criteria at runtime.
It basically acts as a simple plugin mechanism. It allows you to drop python files with a
particular signature (currently: a specified method) into a directory and import all of those
files at runtime.

Usage
-----

The syntax is pretty easy. You provide a directory and the name of a function
and you get a list of modules within that directory that contain the specified
function. These modules are already imported, allowing you to call any method
directly.

The following minimal example should make things clear:

> `from modloader import get_modules`
> 
> `ml = get_modules("./plugins/", "callback")`
> `for mod in ml:`
> `  mod.callback()`

This will execute the `callback()` function for all modules found in the
`plugins` subdirectory. Note that the directory can be given either as an
absolute or a relative path. Both will be handled as expected.

Known Issues
------------

This module does not perform any security checks. It will (try to) import all
modules in a given directory. Potentially, those modules could run any code
even before they are classified as appropriate plugin. All python files within
the specified module directory should, therefore, be trusted.

This module does also not handle any I/O errors (missing directory, files not
readable, files removed during execution, ...). This is on purpose. Anything
going wrong with file access should best be handled by the one who calls this
module.
