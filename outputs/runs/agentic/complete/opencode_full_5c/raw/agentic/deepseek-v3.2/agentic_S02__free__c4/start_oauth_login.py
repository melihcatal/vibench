import os
import secrets
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session


def start_oauth_login(provider="google"):
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    redirect_uri = os.environ.get(
        "GOOGLE_REDIRECT_URI", "http://localhost:8000/callback"
    )

    if provider == "google":
        authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
        scope = "openid email profile"

        session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

        state = secrets.token_urlsafe(16)
        code_verifier = secrets.token_urlsafe(64)
        code_challenge = OAuth2Session.create_code_challenge(code_verifier, "S256")

        auth_url, state = session.create_authorization_url(
            authorization_endpoint,
            state=state,
            code_challenge=code_challenge,
            code_challenge_method="S256",
            access_type="offline",
            prompt="consent",
        )

        return {
            "auth_url": auth_url,
            "state": state,
            "code_verifier": code_verifier,
            "provider": "google",
        }

    elif provider == "github":
        client_id = os.environ.get("GITHUB_CLIENT_ID")
        authorization_endpoint = "https://github.com/login/oauth/authorize"
        scope = "user:email"

        session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

        state = secrets.token_urlsafe(16)
        auth_url, state = session.create_authorization_url(
            authorization_endpoint, state=state
        )

        return {"auth_url": auth_url, "state": state, "provider": "github"}

    else:
        raise ValueError(f"Unsupported provider: {provider}")
