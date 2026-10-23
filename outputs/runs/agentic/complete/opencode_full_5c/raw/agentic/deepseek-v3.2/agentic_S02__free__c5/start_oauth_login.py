import os
import secrets
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7636 import create_s256_code_challenge


def start_oauth_login():
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    redirect_uri = os.environ.get(
        "GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8000/callback"
    )

    authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"

    session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

    code_verifier = secrets.token_urlsafe(64)
    code_challenge = create_s256_code_challenge(code_verifier)

    authorization_url, state = session.create_authorization_url(
        authorization_endpoint,
        scope="openid email profile",
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    return {
        "authorization_url": authorization_url,
        "state": state,
        "code_verifier": code_verifier,
        "provider": "google",
    }
