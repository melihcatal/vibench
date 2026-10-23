import os
from urllib.parse import parse_qs, urlencode, urlparse

import requests


GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def exchange_authorization_code(authorization_code, redirect_uri, code_verifier=None, timeout=10):
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    if client_secret:
        data["client_secret"] = client_secret

    response = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data, timeout=timeout)
    response.raise_for_status()
    return response.json()


def handle_callback(callback_url, expected_state=None, code_verifier=None, timeout=10):
    parsed = urlparse(callback_url)
    params = parse_qs(parsed.query)

    if "error" in params:
        raise ValueError(params["error"][0])

    if expected_state is not None and params.get("state", [None])[0] != expected_state:
        raise ValueError("Invalid state")

    authorization_code = params.get("code", [None])[0]
    if not authorization_code:
        raise ValueError("Missing authorization code")

    redirect_uri = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return exchange_authorization_code(authorization_code, redirect_uri, code_verifier=code_verifier, timeout=timeout)
