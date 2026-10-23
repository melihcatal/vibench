import json
import os
from urllib.parse import parse_qs, urlparse

import requests


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


def exchange_authorization_code(authorization_code: str, redirect_uri: str) -> dict:
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
    payload = {
        "code": authorization_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def handle_callback(callback_url: str, redirect_uri: str) -> dict:
    query = parse_qs(urlparse(callback_url).query)
    code = query.get("code", [None])[0]
    if not code:
        raise ValueError("missing authorization code")
    return exchange_authorization_code(code, redirect_uri)


def main() -> None:
    callback_url = os.environ["CALLBACK_URL"]
    redirect_uri = os.environ["REDIRECT_URI"]
    tokens = handle_callback(callback_url, redirect_uri)
    print(json.dumps(tokens))


if __name__ == "__main__":
    main()
