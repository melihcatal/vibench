import os
import secrets
import urllib.parse


GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_CLIENT_ID_ENV = "GOOGLE_CLIENT_ID"
GOOGLE_REDIRECT_URI_ENV = "GOOGLE_REDIRECT_URI"
GOOGLE_SCOPE_ENV = "GOOGLE_OAUTH_SCOPES"


def build_start_url(state: str | None = None, scopes: str | None = None) -> str:
    client_id = os.environ.get(GOOGLE_CLIENT_ID_ENV, "")
    redirect_uri = os.environ.get(GOOGLE_REDIRECT_URI_ENV, "")
    if not client_id:
        raise ValueError(f"Missing required environment variable: {GOOGLE_CLIENT_ID_ENV}")
    if not redirect_uri:
        raise ValueError(f"Missing required environment variable: {GOOGLE_REDIRECT_URI_ENV}")

    resolved_state = state or secrets.token_urlsafe(32)
    resolved_scopes = scopes or os.environ.get(GOOGLE_SCOPE_ENV, "openid email profile")

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": resolved_scopes,
        "state": resolved_state,
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "consent",
    }
    return f"{GOOGLE_AUTH_ENDPOINT}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"


def start_oauth_login() -> str:
    return build_start_url()


if __name__ == "__main__":
    print(start_oauth_login())
