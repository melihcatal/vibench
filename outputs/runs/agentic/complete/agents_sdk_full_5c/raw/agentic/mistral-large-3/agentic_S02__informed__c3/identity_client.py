import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class OAuthConfig:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    callback_url: Optional[str] = None


def load_auth0_config():
    return OAuthConfig(
        domain=os.getenv("AUTH0_DOMAIN", "https://example.auth0.com"),
        client_id=os.getenv("AUTH0_CLIENT_ID"),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        callback_url=os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")
    )