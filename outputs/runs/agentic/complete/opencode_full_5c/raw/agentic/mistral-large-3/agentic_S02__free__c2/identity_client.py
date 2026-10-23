import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Auth0 Provider Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "your-client-secret")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")


def load_identity_config() -> Dict[str, Any]:
    """Load and return Auth0 identity provider configuration."""
    return {
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "callback_url": AUTH0_CALLBACK_URL,
        "authorization_base_url": f"https://{AUTH0_DOMAIN}/authorize",
        "token_url": f"https://{AUTH0_DOMAIN}/oauth/token",
        "userinfo_url": f"https://{AUTH0_DOMAIN}/userinfo",
        "scope": "openid profile email",
    }


@dataclass
class OAuthTokenResponse:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    token_type: str
    expires_in: int
    scope: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OAuthTokenResponse":
        return cls(
            access_token=data.get("access_token"),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            token_type=data.get("token_type"),
            expires_in=data.get("expires_in"),
            scope=data.get("scope"),
        )
