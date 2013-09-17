# coding=utf-8
import sys, os, logging, re
from inspect import isclass
from os.path import splitext, join, isabs

ERR_IMPORT = "File import of module %s%s has failed."
ERR_MISSINGFUNC = "Module %s lacks function '%s'. Import aborted."
LOGGER = logging.getLogger(__name__)

def find_modules(directory, pattern=None):
    """
        Find all modules within a specified directory. Modules are files that
        end in '.py'. The list can optionally be filtered with a regex matching
        the basename.
    """
    # Create a list of files split into basename and extension
    mfs = [splitext(mf) for mf in os.listdir(directory)]

    # Filter for files ending in '.py'
    mfs = [(mod, ext) for (mod, ext) in mfs if ext == ".py"]

    # Filter for files matching pattern
    if pattern:
        p = re.compile(pattern)
        mfs = [(mod, ext) for (mod, ext) in mfs if p.match(mod)]

    return mfs

def has_function(module, function):
    """
        Checks wether the supplied module has the specified string as function.
    """
    if hasattr(module, function):
        return callable(getattr(module, function))
    else:
        return False

def has_object(module, obj):
    """
        Checks wether the supplied module has a subclass of the specified object.
    """
    objs = []
    for elem in dir(module):
        a = getattr(module, elem)
        if inspect.isclass(a) and issubclass(a, obj):
            return True
    return False

def get_modules(directory, specifier, pattern=None):
    """
        Lade alle Module aus dem Verzeichnis 'directory'

        TODO: Prüfen, dass 'directory' existiert
        TODO: Mehrere Funktionen unterstützen
        TODO: I18N, L10N
    """
    # Add directory to PYTHONPATH
    if isabs(directory):
        sys.path.append(directory)
    else:
        sys.path.append(join(os.getcwd(), directory))

    # Check that 'function' actually exists
    if not specifier:
        raise ValueError("No specifier provided (was empty or 'None')!")

    modulefiles = find_modules(directory, pattern)
    callables = []

    for (modfile, ext) in modulefiles:
        try: # Try to import
            mod_import = __import__(modfile)
        except ImportError:
            LOGGER.error(ERR_IMPORT % (modfile, ext))
            LOGGER.error(sys.exc_info())
        else:
            if (modfile == '__init__'):
                LOGGER.info("Ignore '__init__.py'.")
            # Only accept modules with given function
            elif type(specifier) is str and has_function(mod_import, specifier):
                callables.append(mod_import)
                LOGGER.info('Imported module %s from %s%s.' \
                                        % (mod_import.__name__, modfile, ext))
            elif isclass(specifier) and has_object(mod_import, specifier):
                callables.append(mod_import)
                LOGGER.info('Imported module %s from %s%s.' \
                                        % (mod_import.__name__, modfile, ext))
            else:
                LOGGER.warning(ERR_MISSINGFUNC % (modfile, specifier))
    return callables
