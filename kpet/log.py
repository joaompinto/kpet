from rich import print

from .cli.main import state


def log_verbose(*args, **argv):
    if state.verbose:
        print(*args, **argv)
