from .cli.main import state
from rich import print


def log_verbose(*args, **argv):
    if state.verbose:
        print(*args, **argv)