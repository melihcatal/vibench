import os
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum
from datetime import datetime, timezone


class OAuthProvider(Enum):
    AUTH0 = "auth0"
    AZURE_AD = "azure_ad"
    GOOGLE = "google"
    COGNITO = "cognito"


@dataclass
class OAuthConfig:
    provider: OAuthProvider
    client_id: str
    client_secret: Optional[str] = None
    issuer: str = ""
    authorization_endpoint: str = ""
    token_endpoint: str = ""
    userinfo_endpoint: str = ""
    redirect_uri: str = ""
    scopes: list = field(default_factory=lambda: ["openid", "profile", "email"])
    response_type: str = "code"


@dataclass
class AuthorizationRequest:
    client_id: str
    redirect_uri: str
    scope: str
    response_type: str = "code"
    state: str = ""
    nonce: str = ""
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    prompt: Optional[str] = None
    acr_values: Optional[str] = None

    def to_query_params(self) -> dict:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "response_type": self.response_type,
        }
        if self.state:
            params["state"] = self.state
        if self.nonce:
            params["nonce"] = self.nonce
        if self.code_challenge:
            params["code_challenge"] = self.code_challenge
        if self.code_challenge_method:
            params["code_challenge_method"] = self.code_challenge_method
        if self.prompt:
            params["prompt"] = self.prompt
        if self.acr_values:
            params["acr_values"] = self.acr_values
        return params


@dataclass
class TokenResponse:
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=int(data.get("expires_in", 3600)),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope"),
        )


@dataclass
class NormalizedUserProfile:
    sub: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    phone_number: Optional[str] = None
    raw_claims: dict = field(default_factory=dict)

    @classmethod
    def from_claims(cls, claims: dict) -> "NormalizedUserProfile":
        return cls(
            sub=claims.get("sub", ""),
            email=claims.get("email"),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            phone_number=claims.get("phone_number"),
            raw_claims=claims,
        )


@dataclass
class PKCEPair:
    code_verifier: str
    code_challenge: str
    code_challenge_method: str = "S256"


@dataclass
class CallbackResult:
    tokens: TokenResponse
    profile: Optional[NormalizedUserProfile] = None
    state: Optional[str] = None


@dataclass
class AuditEvent:
    event_id: str
    event_type: str
    timestamp: str
    user_sub: Optional[str] = None
    provider: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    details: dict = field(default_factory=dict)
    claims_snapshot: Optional[dict] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditSummary:
    total_events: int
    successful_logins: int
    failed_logins: int
    providers: dict
    time_range: dict
    top_users: list
    summary_text: str = ""


@dataclass
class ModerationResult:
    text: str
    is_safe: bool
    categories: dict
    confidence_scores: dict
    flagged: bool = False
    details: str = ""


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float = 1.0
