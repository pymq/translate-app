import os
import sys


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by PyInstaller
    return hasattr(sys, "frozen")


def module_path():
    if we_are_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)
