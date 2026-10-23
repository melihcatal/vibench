from dataclasses import dataclass, asdict
from typing import Any
from urllib.parse import urlencode


@dataclass
class AuthorizationRequest:
    authorization_endpoint: str
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    nonce: str
    response_type: str = "code"
    prompt: str | None = None
    code_challenge: str | None = None
    code_challenge_method: str | None = None

    def to_url(self) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": self.state,
            "nonce": self.nonce,
            "response_type": self.response_type,
        }
        if self.prompt:
            params["prompt"] = self.prompt
        if self.code_challenge:
            params["code_challenge"] = self.code_challenge
        if self.code_challenge_method:
            params["code_challenge_method"] = self.code_challenge_method
        return f"{self.authorization_endpoint}?{urlencode(params)}"


@dataclass
class TokenResponse:
    access_token: str | None = None
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None
    scope: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=payload.get("access_token"),
            id_token=payload.get("id_token"),
            refresh_token=payload.get("refresh_token"),
            token_type=payload.get("token_type"),
            expires_in=payload.get("expires_in"),
            scope=payload.get("scope"),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProfileClaims:
    subject: str | None = None
    email: str | None = None
    email_verified: bool | None = None
    full_name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    issuer: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProfileClaims":
        return cls(
            subject=payload.get("sub") or payload.get("subject"),
            email=payload.get("email"),
            email_verified=payload.get("email_verified"),
            full_name=payload.get("name") or payload.get("full_name"),
            given_name=payload.get("given_name"),
            family_name=payload.get("family_name"),
            issuer=payload.get("iss") or payload.get("issuer"),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_token_response(token: TokenResponse) -> TokenResponse:
    return token


def normalize_profile_claims(claims: ProfileClaims) -> ProfileClaims:
    if not claims.full_name and claims.given_name and claims.family_name:
        claims.full_name = f"{claims.given_name} {claims.family_name}".strip()
    return claims
