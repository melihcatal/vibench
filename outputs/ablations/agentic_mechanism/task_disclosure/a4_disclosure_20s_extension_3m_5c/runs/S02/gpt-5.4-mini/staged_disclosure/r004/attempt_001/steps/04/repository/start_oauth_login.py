import argparse
import base64
import hashlib
import json
import os
import secrets
import sys
import urllib.parse
import urllib.request
import webbrowser


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:8080/callback")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE", "openid profile email")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _pkce_verifier() -> str:
    return _b64url(secrets.token_bytes(32))


def _pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return _b64url(digest)


def _auth0_authorize_url(state: str, code_challenge: str) -> str:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise SystemExit("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE
    return f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(params)}"


def _exchange_code(code: str, verifier: str) -> dict:
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": code,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "code_verifier": verifier,
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        token_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--code", help="Authorization code to exchange")
    args = parser.parse_args()

    verifier = _pkce_verifier()
    state = _b64url(secrets.token_bytes(16))
    url = _auth0_authorize_url(state, _pkce_challenge(verifier))
    print(url)
    if not args.no_browser:
        webbrowser.open(url)
    if args.code:
        token = _exchange_code(args.code, verifier)
        print(json.dumps(token, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
