import sys
from typing import Optional

import typer
from rich import print

from kpet.config import KubeConfig


def ctx(
    context_name: Optional[str] = typer.Argument(None, help="Target context name "),
):
    """show or change the current config context"""
    kubeconfig = KubeConfig()
    kubeconfig.load_config()
    if context_name:
        if not kubeconfig.get_context_auth_data(context_name):
            return
        print(f"Switching context to [blue]{context_name}[/]")
        kubeconfig.switch_context(context_name)
        kubeconfig.show_current()
    else:
        for context in kubeconfig.contexts:
            name = context.name
            if sys.stdout.isatty() and kubeconfig.current_context == context.name:
                name = f"{name} [blue]-> current[/]"
            print(f"{name}")
