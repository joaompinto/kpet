import copy
from typing import Optional

import typer
from dinterpol import Template
from rich import print_json

from kpet.config import KubeConfig
from kpet.http import httpx_client_get


def _contains(container: list, content: dict) -> bool:
    for item in container:
        match_count = 0
        for key, value in content.items():
            if item.get(key) == value:
                match_count += 1
        if match_count >= len(content):
            return True
    return False


def exended_symbol(symbol, root_symbol=None, kubeconfig: KubeConfig = None):
    if not isinstance(symbol, dict):
        return symbol
    if root_symbol is None:
        root_symbol = symbol
    symbol_copy = copy.copy(symbol)
    symbol_copy["_"] = root_symbol  # Create a data loopback
    metadata = root_symbol.get("metadata")
    if metadata:
        symbol_copy["_m"] = metadata  # Create a data loopback
        symbol_copy["_n"] = metadata.get("name", "-")  # Create a data loopback
        symbol_copy["_l"] = metadata.get("labels", {})
        symbol_copy["_a"] = metadata.get("annotations", {})
    if "status" in root_symbol.keys():
        symbol_copy["_s"] = root_symbol.get("status", "-")  # Create a data loopback
    if "kubeconfig":
        symbol_copy["_ctx"] = kubeconfig.get_context(kubeconfig.current_context)
    symbol_copy["_contains"] = _contains
    return symbol_copy


def print_data(data):
    if isinstance(data, dict):
        print_json(data=data)
    else:
        print(data)


def print_if_match(kubeconfig, item, template, select_template):
    x = exended_symbol(item["metadata"], item, kubeconfig)
    if select_template:
        result = select_template.render(x)
        if not result:
            return
    if format:
        data = template.render(x)
    else:
        data = item
    print_data(data)


def get(
    context_name: Optional[str] = typer.Option(
        None, "-c", "--ctx", help="Config context to use"
    ),
    endpoint_path: Optional[str] = typer.Argument(
        "", help="Path within the API endpoint"
    ),
    simple_format: Optional[str] = typer.Argument(None, help="Simple format string"),
    format: Optional[str] = typer.Option("", "-f", help="f-string for the output"),
    select: Optional[str] = typer.Option(
        "", "-s", "--select", help="Python expression to for item selection"
    ),
    timeout: Optional[int] = 30,
    insecure: bool = typer.Option(
        False, "--insecure", "-k", help="Ignore SSL validation errors"
    ),
):
    """Perform get into server"""

    kubeconfig = KubeConfig()
    kubeconfig.load_config()
    select_template = None

    if context_name:
        context_name = context_name.strip("\r")

    if select:
        select_template = Template(f"{{{select}}}")

    if simple_format:
        tokens = simple_format.split(" ")
        format = " ".join([f"{{{token}}}" for token in tokens])

    auth_data = kubeconfig.get_context_auth_data(context_name)
    if not auth_data:
        exit(0)

    reply_data = httpx_client_get(auth_data, endpoint_path, timeout, insecure)
    if format or select:
        reply_data = exended_symbol(reply_data, kubeconfig=kubeconfig)
        if "items" in reply_data.keys():
            template = Template(format)
            for item in reply_data["items"]:
                print_if_match(kubeconfig, item, template, select_template)
            return
        reply_data = Template(format).render(reply_data)
    print_data(reply_data)
