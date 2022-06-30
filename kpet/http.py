import httpx
from kpet.log import log_verbose


def httpx_client_get(auth_data, endpoint_path, timeout, insecure):
    if len(auth_data) == 3:
        server, cert, client_ca = auth_data
        if insecure:
            client_ca = False
        http_client = httpx.Client(cert=cert, verify=client_ca, timeout=timeout)
    else:
        server, token = auth_data
        http_client = httpx.Client(
            headers={"Authorization": f"Bearer {token}"},
            timeout=timeout,
            verify=not insecure,
        )

    url = f"{server}/{endpoint_path}"
    log_verbose(f"HTTP GET {url}")
    try:
        response = http_client.get(url)
    except httpx.ConnectTimeout:
        print("[red]Timeout while trying to get answer from server[/]", file=sys.stderr)
        exit(2)
    log_verbose(f"Response {response}", response.text)
    response.raise_for_status()
    return response.json()
