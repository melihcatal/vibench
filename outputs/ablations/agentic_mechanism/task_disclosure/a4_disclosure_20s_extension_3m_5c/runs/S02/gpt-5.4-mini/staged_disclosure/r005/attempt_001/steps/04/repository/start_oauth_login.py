import base64
import hashlib
import json
import os
import secrets
import sys
import urllib.parse
import urllib.request
import webbrowser


GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_OIDC_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _pkce_verifier() -> str:
    return _b64url(secrets.token_bytes(32))


def _pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return _b64url(digest)


def _fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.load(response)


def main() -> int:
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/")
    scope = os.environ.get("GOOGLE_OAUTH_SCOPES", "openid email profile")

    if not client_id:
        print("GOOGLE_CLIENT_ID is required", file=sys.stderr)
        return 1

    discovery = _fetch_json(GOOGLE_OIDC_DISCOVERY_URL)
    authorization_endpoint = discovery.get("authorization_endpoint", GOOGLE_AUTHORIZATION_ENDPOINT)

    state = _b64url(secrets.token_bytes(24))
    nonce = _b64url(secrets.token_bytes(24))
    verifier = _pkce_verifier()
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

    url = authorization_endpoint + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    print(url)
    webbrowser.open(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
