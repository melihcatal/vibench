import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    domain: str
    audience: Optional[str] = None


def get_oauth_config(provider: str) -> OAuthConfig:
    # Auth0 as the concrete provider
    if provider == "auth0":
        return OAuthConfig(
            client_id=os.getenv("AUTH0_CLIENT_ID"),
            client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
            domain=os.getenv("AUTH0_DOMAIN"),
            audience=os.getenv("AUTH0_AUDIENCE"),
        )
    
    raise ValueError(f"Unsupported provider: {provider}")