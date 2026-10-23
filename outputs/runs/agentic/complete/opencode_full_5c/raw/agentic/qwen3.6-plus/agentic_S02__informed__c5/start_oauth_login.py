import os
import secrets
import hashlib
import base64
import time
import urllib.parse

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.environ.get(
    "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
)
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "")
AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE", "openid profile email")


def _auth0_base_url():
    return f"https://{AUTH0_DOMAIN}"


def generate_state():
    return secrets.token_urlsafe(32)


def generate_nonce():
    return secrets.token_urlsafe(32)


def build_authorization_url(state=None, nonce=None, extra_params=None):
    if not state:
        state = generate_state()
    if not nonce:
        nonce = generate_nonce()
    base = _auth0_base_url()
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
    if extra_params:
        params.update(extra_params)
    authorize_url = f"{base}/authorize?{urllib.parse.urlencode(params)}"
    return authorize_url, state, nonce


def start_oauth_login(state=None, nonce=None, extra_params=None):
    authorize_url, state, nonce = build_authorization_url(state, nonce, extra_params)
    return {
        "authorize_url": authorize_url,
        "state": state,
        "nonce": nonce,
        "provider": "auth0",
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "timestamp": time.time(),
    }
