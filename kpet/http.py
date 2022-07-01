import sys

import httpx

from kpet.log import log_verbose


def httpx_client_get(auth_data, endpoint_path, timeout, insecure):
    if len(auth_data) == 3:
        server, cert, client_ca = auth_data
        client_cert_file, client_key_file = cert
        if insecure:
            client_ca = False
        if not client_ca:
            client_ca_str = "-k"
        else:
            client_ca_str = f'--cacert "{client_ca}"'
        http_client = httpx.Client(cert=cert, verify=client_ca, timeout=timeout)
        curl_msg = f'curl {client_ca_str} --cert "{client_cert_file}" --key "{client_key_file}" {server}/'
    else:
        server, token = auth_data
        http_client = httpx.Client(
            headers={"Authorization": f"Bearer {token}"},
            timeout=timeout,
            verify=not insecure,
        )
        curl_msg = f'curl -H "Authorization: Bearer {token}" {server}/'

    url = f"{server}/{endpoint_path}"
    log_verbose(curl_msg)
    try:
        response = http_client.get(url)
    except httpx.ConnectTimeout:
        print("[red]Timeout while trying to get answer from server[/]", file=sys.stderr)
        exit(2)
    log_verbose(f"Response {response}", response.text)
    response.raise_for_status()
    return response.json()
