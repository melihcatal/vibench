import os
import base64
import hashlib
import secrets
from urllib.parse import urlencode

def start_pkce_login_flow():
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').replace('=', '')

    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID")
    redirect_uri = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:3000/callback")

    if not auth0_domain or not auth0_client_id:
        raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set.")

    params = {
        "response_type": "code",
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
        "client_id": auth0_client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "audience": os.environ.get("AUTH0_AUDIENCE")
    }

    authorization_url = f"https://{auth0_domain}/authorize?{urlencode(params)}"
    return authorization_url, code_verifier
