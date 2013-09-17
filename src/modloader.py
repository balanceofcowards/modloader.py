# coding=utf-8
import sys, os, logging, re
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

def get_by_function():
    pass

def get_modules(directory, specifier, pattern=None):
    """
        Lade alle Module aus dem Verzeichnis 'directory'

        TODO: Prüfen, dass 'directory' existiert
        TODO: Mehrere Funktionen unterstützen
        TODO: Klassen unterstützen
        TODO: I18N, L10N
        TODO: Use inspect module
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
    modlist = []

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
            elif (hasattr(mod_import, specifier)):
                if (hasattr(mod_import, "NOEXEC")):
                    if (mod_import.NOEXEC): # NOEXEC? -> Skip module
                        LOGGER.info("Skip module %s." \
                                                % mod_import.__name__)
                        continue
                modlist.append(mod_import)
                LOGGER.info('Imported module %s from %s%s.' \
                                        % (mod_import.__name__, modfile, ext))
            else:
                LOGGER.warning(ERR_MISSINGFUNC % (modfile, specifier))
    return modlist
