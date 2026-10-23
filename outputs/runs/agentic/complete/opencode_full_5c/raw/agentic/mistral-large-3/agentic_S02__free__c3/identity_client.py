import os
from typing import Optional
from dataclasses import dataclass

# Using Auth0 as the OAuth/OIDC provider
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "your-client-secret")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:3000/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")
AUTH0_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")


@dataclass
class OAuthConfig:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    callback_url: Optional[str] = None
    audience: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class PKCERequest:
    code_verifier: str
    code_challenge: str


@dataclass
class TokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


def get_identity_client() -> OAuthConfig:
    """Returns an OAuthConfig instance for Auth0."""
    return OAuthConfig(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        callback_url=AUTH0_CALLBACK_URL,
        audience=AUTH0_AUDIENCE,
        scope=AUTH0_SCOPE,
    )
