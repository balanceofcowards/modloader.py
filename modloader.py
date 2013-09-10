# coding=utf-8
import sys, os, logging
from os.path import splitext, join, isabs

ERR_IMPORT = "File import of module %s%s has failed."
ERR_MISSINGFUNC = "Module %s lacks function '%s'. Import aborted."
LOGGER = logging.getLogger(__name__)

def get_modules(directory, function):
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

    # Create a list of files split into basename and extension
    modulefiles = [splitext(mfile) for mfile in os.listdir(directory)]

    # Filter for files ending in '.py'
    modulefiles = [(mfile, ext) for (mfile, ext) in modulefiles if ext == ".py"]

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
            elif (hasattr(mod_import, function)):
                if (hasattr(mod_import, "NOEXEC")):
                    if (mod_import.NOEXEC): # NOEXEC? -> Skip module
                        LOGGER.info("Skip module %s." \
                                                % mod_import.__name__)
                        continue
                modlist.append(mod_import)
                LOGGER.info('Imported module %s from %s%s.' \
                                        % (mod_import.__name__, modfile, ext))
            else:
                LOGGER.warning(ERR_MISSINGFUNC % (modfile, function))
    return modlist
