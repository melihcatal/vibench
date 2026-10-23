import os
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode


@dataclass
class OAuthConfig:
    provider: str = "auth0"
    domain: str = field(default_factory=lambda: os.environ.get("AUTH0_DOMAIN", ""))
    client_id: str = field(
        default_factory=lambda: os.environ.get("AUTH0_CLIENT_ID", "")
    )
    client_secret: str = field(
        default_factory=lambda: os.environ.get("AUTH0_CLIENT_SECRET", "")
    )
    redirect_uri: str = field(
        default_factory=lambda: os.environ.get(
            "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
        )
    )
    audience: str = field(default_factory=lambda: os.environ.get("AUTH0_AUDIENCE", ""))
    issuer: str = ""
    authorization_endpoint: str = ""
    token_endpoint: str = ""
    userinfo_endpoint: str = ""
    scope: str = "openid profile email"

    def __post_init__(self):
        if not self.issuer:
            self.issuer = f"https://{self.domain}/"
        if not self.authorization_endpoint:
            self.authorization_endpoint = f"https://{self.domain}/authorize"
        if not self.token_endpoint:
            self.token_endpoint = f"https://{self.domain}/oauth/token"
        if not self.userinfo_endpoint:
            self.userinfo_endpoint = f"https://{self.domain}/userinfo"


@dataclass
class PKCEState:
    code_verifier: str = ""
    code_challenge: str = ""
    code_challenge_method: str = "S256"
    state: str = ""


@dataclass
class TokenResponse:
    access_token: str = ""
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserProfile:
    sub: str = ""
    name: str = ""
    email: str = ""
    email_verified: bool = False
    picture: str = ""
    nickname: str = ""
    updated_at: str = ""
    provider: str = ""
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditEvent:
    event_id: str = ""
    event_type: str = ""
    timestamp: str = ""
    user_sub: str = ""
    provider: str = ""
    ip_address: str = ""
    user_agent: str = ""
    success: bool = True
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_authorization_url(
    config: OAuthConfig,
    state: str,
    nonce: str,
    pkce_state: Optional[PKCEState] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> str:
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "state": state,
        "nonce": nonce,
    }
    if config.audience:
        params["audience"] = config.audience
    if pkce_state:
        params["code_challenge"] = pkce_state.code_challenge
        params["code_challenge_method"] = pkce_state.code_challenge_method
    if extra_params:
        params.update(extra_params)
    return f"{config.authorization_endpoint}?{urlencode(params)}"


def normalize_profile_claims(
    raw_claims: Dict[str, Any], provider: str = "auth0"
) -> UserProfile:
    profile = UserProfile(
        sub=raw_claims.get("sub", ""),
        name=raw_claims.get("name", ""),
        email=raw_claims.get("email", ""),
        email_verified=raw_claims.get("email_verified", False),
        picture=raw_claims.get("picture", ""),
        nickname=raw_claims.get("nickname", raw_claims.get("preferred_username", "")),
        updated_at=raw_claims.get("updated_at", ""),
        provider=provider,
        raw_claims=raw_claims,
    )
    return profile


def build_token_request_payload(
    config: OAuthConfig,
    code: str,
    code_verifier: Optional[str] = None,
) -> Dict[str, str]:
    payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": config.redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    return payload


def parse_token_response(response_data: Dict[str, Any]) -> TokenResponse:
    return TokenResponse(
        access_token=response_data.get("access_token", ""),
        id_token=response_data.get("id_token", ""),
        refresh_token=response_data.get("refresh_token", ""),
        token_type=response_data.get("token_type", "Bearer"),
        expires_in=response_data.get("expires_in", 0),
        scope=response_data.get("scope", ""),
    )
