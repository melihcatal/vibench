import os
import secrets
import urllib.parse
from typing import Dict, Optional


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost:8000/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
AUTH0_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")


def _build_authorize_url(state: str, nonce: str, extras: Optional[Dict[str, str]] = None) -> str:
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "state": state,
        "nonce": nonce,
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE
    if extras:
        params.update({k: v for k, v in extras.items() if v is not None})
    return f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(params)}"


def start_oauth_login(additional_parameters: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)
    authorize_url = _build_authorize_url(state, nonce, additional_parameters)
    return {
        "provider": "Auth0",
        "authorize_url": authorize_url,
        "state": state,
        "nonce": nonce,
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
    }


if __name__ == "__main__":
    result = start_oauth_login()
    print(result["authorize_url"])
