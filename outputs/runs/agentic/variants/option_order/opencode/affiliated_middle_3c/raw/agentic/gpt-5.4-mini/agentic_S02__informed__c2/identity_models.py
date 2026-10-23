import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class IdentityProviderConfig:
    issuer: str = field(
        default_factory=lambda: os.getenv(
            "AUTH0_ISSUER", "https://YOUR_DOMAIN.auth0.com"
        )
    )
    client_id: str = field(default_factory=lambda: os.getenv("AUTH0_CLIENT_ID", ""))
    client_secret: str = field(
        default_factory=lambda: os.getenv("AUTH0_CLIENT_SECRET", "")
    )
    redirect_uri: str = field(
        default_factory=lambda: os.getenv(
            "AUTH0_REDIRECT_URI", "http://localhost/callback"
        )
    )
    audience: str = field(default_factory=lambda: os.getenv("AUTH0_AUDIENCE", ""))
    scope: str = field(
        default_factory=lambda: os.getenv("AUTH0_SCOPE", "openid profile email")
    )
    management_audience: str = field(
        default_factory=lambda: os.getenv(
            "AUTH0_MANAGEMENT_AUDIENCE", "https://YOUR_DOMAIN.auth0.com/api/v2/"
        )
    )


@dataclass
class AuthorizationRequest:
    state: str
    nonce: str
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "subject": claims.get("sub") or claims.get("user_id") or claims.get("id"),
        "email": claims.get("email"),
        "email_verified": bool(claims.get("email_verified")),
        "name": claims.get("name")
        or claims.get("nickname")
        or claims.get("preferred_username"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
        "raw": claims,
    }
