from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass
class IdentityProviderConfig:
    tenant_id: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    authority: str = "https://login.microsoftonline.com"
    scope: str = "openid profile email User.Read"


@dataclass
class AuthorizationRequest:
    state: str
    nonce: str
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class FederatedProfile:
    subject: str
    display_name: Optional[str] = None
    email: Optional[str] = None
    issuer: Optional[str] = None
    claims: Optional[Dict[str, Any]] = None


def normalize_profile_claims(claims: Mapping[str, Any]) -> FederatedProfile:
    subject = str(claims.get("sub") or claims.get("oid") or claims.get("id") or "")
    display_name = claims.get("name") or claims.get("preferred_username") or claims.get("given_name")
    email = claims.get("email") or claims.get("preferred_username") or claims.get("upn")
    issuer = claims.get("iss")
    return FederatedProfile(subject=subject, display_name=display_name, email=email, issuer=issuer, claims=dict(claims))
