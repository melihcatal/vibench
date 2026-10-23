import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    authorize_url: str
    token_url: str
    userinfo_url: str
    audience: Optional[str] = None


def get_oauth_config(provider: str) -> OAuthConfig:
    if provider == "auth0":
        return OAuthConfig(
            client_id=os.getenv("AUTH0_CLIENT_ID"),
            client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
            authorize_url="https://dev-abc123.auth0.com/authorize",
            token_url="https://dev-abc123.auth0.com/oauth/token",
            userinfo_url="https://dev-abc123.auth0.com/userinfo",
            audience=os.getenv("AUTH0_AUDIENCE", "https://dev-abc123.auth0.com/api/v2/"),
        )
    elif provider == "okta":
        return OAuthConfig(
            client_id=os.getenv("OKTA_CLIENT_ID"),
            client_secret=os.getenv("OKTA_CLIENT_SECRET"),
            authorize_url="https://dev-123456.okta.com/oauth2/default/v1/authorize",
            token_url="https://dev-123456.okta.com/oauth2/default/v1/token",
            userinfo_url="https://dev-123456.okta.com/oauth2/default/v1/userinfo",
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")