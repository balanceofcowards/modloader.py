# coding=utf-8
import sys, os, logging
from os.path import splitext, join

ERR_IMPORT = "Dateiimport von %s%s fehlgeschlagen."
ERR_MISSINGFUNC = "Modul %s hat keine %s-Funktion. Import abgebrochen."
LOGGER = logging.getLogger(__name__)

def get_modules(directory, function):
    """
        Lade alle Module aus dem Verzeichnis 'directory'

        TODO: Prüfen, dass 'directory' existiert
        TODO: Mehrere Funktionen unterstützen
    """
    # Das Verzeichnis zum PYTHONPATH hinzufügen
    sys.path.append(join(os.getcwd(), directory))

    # Zerteile die Dateinamen in Basisname und Erweiterung
    modulefiles = [splitext(mfile) for mfile in os.listdir(directory)]

    # Filtere alle Dateien, die nicht auf ".py" enden aus der Liste
    modulefiles = [(mfile, ext) for (mfile, ext) in modulefiles if ext == ".py"]

    modlist = []
    for (modfile, ext) in modulefiles:
        try: # Versuche Import
            mod_import = __import__(modfile)
        except ImportError:
            LOGGER.error(ERR_IMPORT % (modfile, ext))
            LOGGER.error(sys.exc_info())
        else:
            if (modfile == '__init__'):
                LOGGER.info('__init__.py ignoriert')
            # Nur Module mit oben übergebener Funktion werden akzeptiert
            elif (hasattr(mod_import, function)):
                if (hasattr(mod_import, "NOEXEC")):
                    if (mod_import.NOEXEC): # NOEXEC? -> Modul auslassen
                        LOGGER.info("Modul %s ausgelassen" \
                                                % mod_import.__name__)
                        continue
                modlist.append(mod_import)
                LOGGER.info('Modul %s aus %s%s importiert.' \
                                        % (mod_import.__name__, modfile, ext))
            else:
                LOGGER.warning(ERR_MISSINGFUNC % (modfile, function))
    return modlist
