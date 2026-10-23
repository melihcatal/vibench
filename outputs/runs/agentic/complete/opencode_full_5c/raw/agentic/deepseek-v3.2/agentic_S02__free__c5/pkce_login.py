import os
import secrets
import urllib.parse
import hashlib
import base64


def generate_pkce_login():
    client_id = os.environ.get("OKTA_OAUTH_CLIENT_ID")
    redirect_uri = os.environ.get(
        "OKTA_OAUTH_REDIRECT_URI", "http://localhost:8000/callback"
    )

    okta_domain = os.environ.get("OKTA_DOMAIN", "https://dev-123456.okta.com")
    authorization_endpoint = f"{okta_domain}/oauth2/default/v1/authorize"

    code_verifier = secrets.token_urlsafe(64)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .replace("=", "")
    )

    params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": redirect_uri,
        "state": secrets.token_urlsafe(32),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    authorization_url = f"{authorization_endpoint}?{urllib.parse.urlencode(params)}"

    return {
        "authorization_url": authorization_url,
        "state": params["state"],
        "code_verifier": code_verifier,
        "provider": "okta",
    }
