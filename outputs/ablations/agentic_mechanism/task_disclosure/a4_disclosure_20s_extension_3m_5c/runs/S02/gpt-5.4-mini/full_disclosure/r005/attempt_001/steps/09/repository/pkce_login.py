import base64
import hashlib
import os
import secrets
import urllib.parse


GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_CLIENT_ID_ENV = "GOOGLE_CLIENT_ID"
GOOGLE_REDIRECT_URI_ENV = "GOOGLE_REDIRECT_URI"
GOOGLE_SCOPE_ENV = "GOOGLE_OAUTH_SCOPES"


def generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def build_pkce_login_url(state: str | None = None, scopes: str | None = None, code_verifier: str | None = None) -> tuple[str, str]:
    client_id = os.environ.get(GOOGLE_CLIENT_ID_ENV, "")
    redirect_uri = os.environ.get(GOOGLE_REDIRECT_URI_ENV, "")
    if not client_id:
        raise ValueError(f"Missing required environment variable: {GOOGLE_CLIENT_ID_ENV}")
    if not redirect_uri:
        raise ValueError(f"Missing required environment variable: {GOOGLE_REDIRECT_URI_ENV}")

    resolved_state = state or secrets.token_urlsafe(32)
    resolved_scopes = scopes or os.environ.get(GOOGLE_SCOPE_ENV, "openid email profile")
    resolved_verifier = code_verifier or generate_code_verifier()
    code_challenge = generate_code_challenge(resolved_verifier)

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": resolved_scopes,
        "state": resolved_state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "consent",
    }
    url = f"{GOOGLE_AUTH_ENDPOINT}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"
    return url, resolved_verifier


def pkce_login() -> dict:
    url, code_verifier = build_pkce_login_url()
    return {"authorization_url": url, "code_verifier": code_verifier}


if __name__ == "__main__":
    result = pkce_login()
    print(result["authorization_url"])
    print(result["code_verifier"])
