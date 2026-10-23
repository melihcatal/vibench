import base64
import hashlib
import os
import secrets
import urllib.parse


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost:8000/callback")
AUTH0_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _pkce_verifier() -> str:
    return _b64url(secrets.token_bytes(32))


def _pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return _b64url(digest)


def build_authorization_url(state: str | None = None):
    verifier = _pkce_verifier()
    challenge = _pkce_challenge(verifier)
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "state": state or _b64url(secrets.token_bytes(16)),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE
    query = urllib.parse.urlencode(params)
    return f"https://{AUTH0_DOMAIN}/authorize?{query}", verifier


def start_oauth_login(state: str | None = None):
    return build_authorization_url(state)


if __name__ == "__main__":
    url, verifier = start_oauth_login()
    print(url)
    print(verifier)
