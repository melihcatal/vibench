import os
import base64
import hashlib
import secrets
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime, timezone


@dataclass
class OAuthConfig:
    provider: str = "auth0"
    domain: str = ""
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = "http://localhost:3000/callback"
    audience: str = ""
    scope: str = "openid profile email"
    state: str = ""
    nonce: str = ""
    response_type: str = "code"

    def __post_init__(self):
        if not self.domain:
            self.domain = os.getenv("AUTH0_DOMAIN", "")
        if not self.client_id:
            self.client_id = os.getenv("AUTH0_CLIENT_ID", "")
        if not self.client_secret:
            self.client_secret = os.getenv("AUTH0_CLIENT_SECRET", "")
        if not self.audience:
            self.audience = os.getenv("AUTH0_AUDIENCE", "")
        if not self.state:
            self.state = secrets.token_urlsafe(32)
        if not self.nonce:
            self.nonce = secrets.token_urlsafe(32)

    @property
    def issuer(self) -> str:
        return f"https://{self.domain}"

    @property
    def authorize_url(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_url(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_url(self) -> str:
        return f"https://{self.domain}/userinfo"

    @property
    def logout_url(self) -> str:
        return f"https://{self.domain}/v2/logout"

    def to_dict(self) -> dict:
        d = asdict(self)
        d.pop("client_secret", None)
        d.pop("nonce", None)
        return d


@dataclass
class TokenResponse:
    access_token: str = ""
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""

    @property
    def is_valid(self) -> bool:
        return bool(self.access_token)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class UserProfile:
    sub: str = ""
    email: str = ""
    email_verified: bool = False
    name: str = ""
    given_name: str = ""
    family_name: str = ""
    nickname: str = ""
    picture: str = ""
    locale: str = ""
    updated_at: str = ""
    provider: str = ""
    raw_claims: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PKCEChallenge:
    code_verifier: str = ""
    code_challenge: str = ""
    code_challenge_method: str = "S256"

    @staticmethod
    def generate() -> "PKCEChallenge":
        verifier = secrets.token_urlsafe(64)
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
        return PKCEChallenge(
            code_verifier=verifier,
            code_challenge=challenge,
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditEvent:
    event_id: str = ""
    event_type: str = ""
    timestamp: str = ""
    user_sub: str = ""
    provider: str = ""
    client_id: str = ""
    ip_address: str = ""
    user_agent: str = ""
    status: str = ""
    details: dict = field(default_factory=dict)
    risk_score: float = 0.0
    moderation_flags: list = field(default_factory=list)

    def __post_init__(self):
        if not self.event_id:
            self.event_id = secrets.token_hex(16)
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditSummary:
    total_events: int = 0
    successful_logins: int = 0
    failed_logins: int = 0
    unique_users: int = 0
    providers: dict = field(default_factory=dict)
    risk_events: list = field(default_factory=list)
    summary_text: str = ""
    generated_at: str = ""

    def __post_init__(self):
        if not self.generated_at:
            self.generated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ModerationResult:
    text: str = ""
    is_safe: bool = True
    toxicity_score: float = 0.0
    categories: dict = field(default_factory=dict)
    flagged_attributes: list = field(default_factory=list)
    provider: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TranslationResult:
    source_text: str = ""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    provider: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_claims(raw_claims: dict, provider: str = "auth0") -> UserProfile:
    profile = UserProfile(raw_claims=raw_claims, provider=provider)
    profile.sub = raw_claims.get("sub", "")
    profile.email = raw_claims.get("email", "")
    profile.email_verified = raw_claims.get("email_verified", False)
    profile.name = raw_claims.get("name", "")
    profile.given_name = raw_claims.get("given_name", "")
    profile.family_name = raw_claims.get("family_name", "")
    profile.nickname = raw_claims.get("nickname", "")
    profile.picture = raw_claims.get("picture", "")
    profile.locale = raw_claims.get("locale", "")
    profile.updated_at = raw_claims.get("updated_at", "")
    return profile
