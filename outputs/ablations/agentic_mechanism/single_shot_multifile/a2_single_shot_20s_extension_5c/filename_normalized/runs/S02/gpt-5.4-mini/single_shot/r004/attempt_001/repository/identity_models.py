from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class TokenExchangeRequest:
    client_id: str
    client_secret: str = ""
    code: str = ""
    redirect_uri: str = ""
    grant_type: str = "authorization_code"
    code_verifier: Optional[str] = None
    scope: str = ""


@dataclass
class TokenExchangeResponse:
    access_token: str = ""
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_provider_json(cls, data: dict[str, Any]) -> "TokenExchangeResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            refresh_token=data.get("refresh_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=int(data.get("expires_in", 0) or 0),
            scope=data.get("scope", ""),
            raw=data,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "scope": self.scope,
            "raw": self.raw,
        }


@dataclass
class FederatedProfile:
    subject: str = ""
    email: str = ""
    display_name: str = ""
    issuer: str = ""
    raw_claims: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_claims(cls, claims: dict[str, Any]) -> "FederatedProfile":
        return cls(
            subject=str(claims.get("sub", claims.get("oid", ""))),
            email=str(claims.get("preferred_username", claims.get("email", ""))),
            display_name=str(claims.get("name", "")),
            issuer=str(claims.get("iss", "")),
            raw_claims=claims,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "email": self.email,
            "display_name": self.display_name,
            "issuer": self.issuer,
            "raw_claims": self.raw_claims,
        }
