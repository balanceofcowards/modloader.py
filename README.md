modloader.py
============

Description
-----------

Provides functionality to load a bunch of python modules matching a certain criteria at runtime.
It basically acts as a simple plugin mechanism. It allows you to drop python files matching a
certain criteria (currently: either defining a particular function or a subclass of a given
class) into a directory and import all of those files at runtime.

Usage
-----

The syntax is pretty easy. You provide a directory and a specifier and you get a list of all
modules containing the respective callable elements which you can then execute directly.
The specifier can be either a string representing a
function name or a class. In the first case, all modules containing a function with the same
name will be provided. In the second case, all modules defining a subclass of the given object
 will be returned. In both cases it will be possible to call any element of the list just by
`elem.specifier()`.

The following minimal example should make things clear:

```Python
from modloader import get_modules

funcs = get_modules("./plugins/", "callback")
for f in funcs:
  f()
```

This will execute the `callback()` function (redubbed "f" in the loop) for all modules found
in the `plugins` subdirectory. Note that the directory can be given either as an
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

Bugs
----

The current concept for module loading via classes doesn't work as envisioned, yet. While the
correct classes are loaded, the user currently has to find the correct classname himself. This
is made even more complicated as modules can contain any number of subclasses of any given class
(whereas they can only contain one function with a certain name). Needs more thought.
