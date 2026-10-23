import os
from .identity_models import OAuthConfig


def get_google_confidential_config() -> OAuthConfig:
    return OAuthConfig(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback"),
        auth_url="https://accounts.google.com/o/oauth2/v2/auth",
        token_url="https://oauth2.googleapis.com/token",
        scopes=["openid", "email", "profile"],
    )


def get_google_pkce_config() -> OAuthConfig:
    return OAuthConfig(
        client_id=os.getenv("GOOGLE_PKCE_CLIENT_ID"),
        client_secret=None,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback"),
        auth_url="https://accounts.google.com/o/oauth2/v2/auth",
        token_url="https://oauth2.googleapis.com/token",
        scopes=["openid", "email", "profile"],
    )
