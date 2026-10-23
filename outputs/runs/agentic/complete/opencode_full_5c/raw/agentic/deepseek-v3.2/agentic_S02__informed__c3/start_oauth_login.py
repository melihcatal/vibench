import os
import secrets
import hashlib
import base64
import urllib.parse
from auth0.authentication import GetToken
from auth0.management import Auth0


def generate_auth_url():
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    redirect_uri = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
    )

    if not domain or not client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables are required"
        )

    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)

    auth_url = f"https://{domain}/authorize"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
        "nonce": nonce,
    }

    full_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return {"auth_url": full_url, "state": state, "nonce": nonce}


def start_oidc_login():
    try:
        result = generate_auth_url()
        print(f"Redirect user to: {result['auth_url']}")
        return result
    except Exception as e:
        print(f"Error starting OIDC login: {e}")
        raise
