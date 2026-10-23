from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class IdentityProviderConfig:
    issuer: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    authorization_endpoint: Optional[str] = None
    token_endpoint: Optional[str] = None
    userinfo_endpoint: Optional[str] = None
    jwks_uri: Optional[str] = None
    scope: str = "openid email profile"


@dataclass
class AuthorizationRequest:
    state: str
    nonce: str
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    redirect_uri: Optional[str] = None


@dataclass
class TokenSet:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    issuer: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_profile_claims(claims: Dict[str, Any], issuer: Optional[str] = None) -> FederatedProfile:
    subject = str(claims.get("sub", ""))
    return FederatedProfile(
        subject=subject,
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        issuer=issuer or claims.get("iss"),
        raw=claims,
    )
