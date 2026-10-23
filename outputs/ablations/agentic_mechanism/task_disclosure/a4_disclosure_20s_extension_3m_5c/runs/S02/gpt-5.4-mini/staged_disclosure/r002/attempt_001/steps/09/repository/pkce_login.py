import base64
import hashlib
import json
import os
import secrets
import sys
import urllib.parse
import urllib.request


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI", "http://127.0.0.1:8000/callback")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _pkce_pair() -> tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def _authorize_url(state: str, challenge: str) -> str:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise RuntimeError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": "openid profile email offline_access",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE
    return f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(params)}"


def exchange_code(code: str, verifier: str) -> dict:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise RuntimeError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")
    data = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "client_id": AUTH0_CLIENT_ID,
            "code": code,
            "code_verifier": verifier,
            "redirect_uri": AUTH0_REDIRECT_URI,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    verifier, challenge = _pkce_pair()
    state = _b64url(secrets.token_bytes(16))
    url = _authorize_url(state, challenge)
    print(url)
    code = input("Authorization code: ").strip()
    if not code:
        return 1
    token_response = exchange_code(code, verifier)
    print(json.dumps(token_response, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
