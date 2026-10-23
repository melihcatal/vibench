import os
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    authorize_url: str
    access_token_url: str
    api_base_url: str
    scope: str
    audience: Optional[str] = None


def load_auth0_config() -> OAuthConfig:
    return OAuthConfig(
        client_id=os.getenv("AUTH0_CLIENT_ID"),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        authorize_url="https://dev-12345678.auth0.com/authorize",
        access_token_url="https://dev-12345678.auth0.com/oauth/token",
        api_base_url="https://dev-12345678.auth0.com/",
        scope="openid profile email",
        audience=os.getenv("AUTH0_AUDIENCE"),
    )


def normalize_token_response(token: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "access_token": token.get("access_token"),
        "refresh_token": token.get("refresh_token"),
        "id_token": token.get("id_token"),
        "token_type": token.get("token_type"),
        "expires_in": token.get("expires_in"),
        "expires_at": token.get("expires_at"),
    }
