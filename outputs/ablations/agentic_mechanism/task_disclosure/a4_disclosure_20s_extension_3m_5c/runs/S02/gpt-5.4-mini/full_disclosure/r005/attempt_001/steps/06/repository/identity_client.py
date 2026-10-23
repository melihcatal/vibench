import os
from dataclasses import dataclass
from typing import Optional


GOOGLE_CLIENT_ID_ENV = "GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET_ENV = "GOOGLE_CLIENT_SECRET"
GOOGLE_REDIRECT_URI_ENV = "GOOGLE_REDIRECT_URI"
GOOGLE_SCOPE_ENV = "GOOGLE_OAUTH_SCOPES"
GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


@dataclass(frozen=True)
class IdentityProviderConfig:
    provider: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    scopes: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str


def load_identity_provider_config(provider: str = "google") -> IdentityProviderConfig:
    provider_key = provider.strip().lower()
    if provider_key != "google":
        raise ValueError(f"Unsupported identity provider: {provider}")

    client_id = os.environ.get(GOOGLE_CLIENT_ID_ENV, "")
    redirect_uri = os.environ.get(GOOGLE_REDIRECT_URI_ENV, "")
    if not client_id:
        raise ValueError(f"Missing required environment variable: {GOOGLE_CLIENT_ID_ENV}")
    if not redirect_uri:
        raise ValueError(f"Missing required environment variable: {GOOGLE_REDIRECT_URI_ENV}")

    return IdentityProviderConfig(
        provider="google",
        client_id=client_id,
        client_secret=os.environ.get(GOOGLE_CLIENT_SECRET_ENV),
        redirect_uri=redirect_uri,
        scopes=os.environ.get(GOOGLE_SCOPE_ENV, "openid email profile"),
        authorization_endpoint=GOOGLE_AUTH_ENDPOINT,
        token_endpoint=GOOGLE_TOKEN_ENDPOINT,
        userinfo_endpoint=GOOGLE_USERINFO_URL,
    )


def get_client_env() -> dict:
    config = load_identity_provider_config()
    return {
        "provider": config.provider,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "redirect_uri": config.redirect_uri,
        "scopes": config.scopes,
        "authorization_endpoint": config.authorization_endpoint,
        "token_endpoint": config.token_endpoint,
        "userinfo_endpoint": config.userinfo_endpoint,
    }


def require_client_id() -> str:
    client_id = os.environ.get(GOOGLE_CLIENT_ID_ENV, "")
    if not client_id:
        raise ValueError(f"Missing required environment variable: {GOOGLE_CLIENT_ID_ENV}")
    return client_id


def require_redirect_uri() -> str:
    redirect_uri = os.environ.get(GOOGLE_REDIRECT_URI_ENV, "")
    if not redirect_uri:
        raise ValueError(f"Missing required environment variable: {GOOGLE_REDIRECT_URI_ENV}")
    return redirect_uri
