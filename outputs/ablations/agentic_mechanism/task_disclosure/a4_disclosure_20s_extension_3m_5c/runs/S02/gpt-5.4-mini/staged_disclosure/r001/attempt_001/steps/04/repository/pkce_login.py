import base64
import hashlib
import os
import secrets
import sys
import urllib.parse
import webbrowser

import requests


AUTHORIZATION_ENDPOINT = "https://github.com/login/oauth/authorize"
TOKEN_ENDPOINT = "https://github.com/login/oauth/access_token"
CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
REDIRECT_URI = os.environ.get("GITHUB_REDIRECT_URI", "http://localhost:8080/callback")
SCOPE = os.environ.get("GITHUB_SCOPE", "read:user")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_code_verifier() -> str:
    return _b64url(secrets.token_bytes(32))


def generate_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return _b64url(digest)


def build_authorization_url(state: str, code_challenge: str) -> str:
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state,
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(code: str, verifier: str) -> dict:
    headers = {"Accept": "application/json"}
    data = {
        "client_id": CLIENT_ID,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": verifier,
    }
    response = requests.post(TOKEN_ENDPOINT, headers=headers, data=data, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> int:
    if not CLIENT_ID:
        print("GITHUB_CLIENT_ID is required", file=sys.stderr)
        return 1

    verifier = generate_code_verifier()
    state = _b64url(secrets.token_bytes(16))
    url = build_authorization_url(state, generate_code_challenge(verifier))
    print(url)
    try:
        webbrowser.open(url)
    except Exception:
        pass

    code = input("Enter the authorization code: ").strip()
    token = exchange_code_for_token(code, verifier)
    print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
