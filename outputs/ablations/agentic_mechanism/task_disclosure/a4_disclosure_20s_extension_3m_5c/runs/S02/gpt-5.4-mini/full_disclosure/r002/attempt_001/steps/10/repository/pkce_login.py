import base64
import hashlib
import os
import secrets
import urllib.parse

AUTH0_AUTHORIZE_URL = "https://dev-tenant.us.auth0.com/authorize"
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:8000/callback")
AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE", "openid profile email")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_pkce_pair() -> tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def build_authorization_url(state: str | None = None) -> tuple[str, str, str]:
    if not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_CLIENT_ID is required")
    verifier, challenge = generate_pkce_pair()
    query = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if state is None:
        state = _b64url(secrets.token_bytes(16))
    query["state"] = state
    url = f"{AUTH0_AUTHORIZE_URL}?{urllib.parse.urlencode(query)}"
    return url, verifier, state


def create_pkce_login_request() -> dict[str, str]:
    url, verifier, state = build_authorization_url()
    return {"authorization_url": url, "code_verifier": verifier, "state": state, "provider": "Auth0"}
