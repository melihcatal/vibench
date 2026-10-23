from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class OAuthLoginRequest:
    redirect_uri: Optional[str] = None
    scope: Optional[str] = None
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass
class OAuthLoginResponse:
    authorization_url: str
    state: str
    nonce: str


@dataclass
class OAuthCallbackRequest:
    code: str
    state: str
    redirect_uri: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    scope: Optional[str] = None


@dataclass
class PKCELoginRequest:
    redirect_uri: Optional[str] = None
    scope: Optional[str] = None
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None


@dataclass
class PKCELoginResponse:
    authorization_url: str
    state: str
    code_verifier: str


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_claims(cls, claims: Dict[str, Any]) -> "FederatedProfile":
        return cls(
            subject=str(claims.get("sub") or claims.get("jwt_subject") or ""),
            email=claims.get("email"),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            raw_claims=claims,
        )
