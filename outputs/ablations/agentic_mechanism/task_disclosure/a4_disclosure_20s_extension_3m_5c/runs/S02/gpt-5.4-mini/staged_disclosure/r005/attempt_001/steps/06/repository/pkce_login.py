import base64
import hashlib
import json
import os
import secrets
import sys
import urllib.parse
import urllib.request
import webbrowser


GOOGLE_OIDC_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _pkce_verifier() -> str:
    return _b64url(secrets.token_bytes(32))


def _pkce_challenge(verifier: str) -> str:
    return _b64url(hashlib.sha256(verifier.encode("ascii")).digest())


def _fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.load(response)


def _build_authorization_url(client_id: str, redirect_uri: str, scope: str, verifier: str) -> tuple[str, str, str]:
    discovery = _fetch_json(GOOGLE_OIDC_DISCOVERY_URL)
    authorization_endpoint = discovery.get("authorization_endpoint", GOOGLE_AUTHORIZATION_ENDPOINT)
    state = _b64url(secrets.token_bytes(24))
    nonce = _b64url(secrets.token_bytes(24))
    challenge = _pkce_challenge(verifier)
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
        "nonce": nonce,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
        "prompt": "consent",
    }
    return authorization_endpoint + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote), state, nonce


def exchange_authorization_code(code: str, redirect_uri: str, verifier: str) -> dict:
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    payload = {
        "code": code,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code_verifier": verifier,
    }
    if client_secret:
        payload["client_secret"] = client_secret
    request = urllib.request.Request(
        GOOGLE_TOKEN_ENDPOINT,
        data=urllib.parse.urlencode(payload).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/")
    scope = os.environ.get("GOOGLE_OAUTH_SCOPES", "openid email profile")
    if not client_id:
        print("GOOGLE_CLIENT_ID is required", file=sys.stderr)
        return 1
    verifier = _pkce_verifier()
    url, state, nonce = _build_authorization_url(client_id, redirect_uri, scope, verifier)
    print(url)
    print(state)
    print(nonce)
    print(verifier)
    webbrowser.open(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
