import os
import base64
import hashlib
import secrets
import requests
from typing import Dict, Optional, Tuple
from identity_models import (
    OAuthConfig,
    AuthorizationRequest,
    TokenResponse,
    UserProfile,
    NormalizedClaims,
    PkcePair,
)


def load_oauth_config() -> OAuthConfig:
    return OAuthConfig(
        domain=os.getenv("AUTH0_DOMAIN", ""),
        client_id=os.getenv("AUTH0_CLIENT_ID", ""),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET", ""),
        redirect_uri=os.getenv("AUTH0_REDIRECT_URI", "http://localhost:3000/callback"),
        audience=os.getenv("AUTH0_AUDIENCE", ""),
        scope=os.getenv("AUTH0_SCOPE", "openid profile email"),
    )


def build_authorization_url(
    config: OAuthConfig,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: str = "S256",
    connection: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> Tuple[str, str]:
    req = AuthorizationRequest(
        client_id=config.client_id,
        redirect_uri=config.redirect_uri,
        response_type="code",
        scope=config.scope,
        state=state or secrets.token_urlsafe(32),
        nonce=nonce or secrets.token_urlsafe(32),
        audience=config.audience,
        code_challenge=code_challenge or "",
        code_challenge_method=code_challenge_method if code_challenge else "",
        connection=connection or "",
    )
    params = req.to_query_params()
    if extra_params:
        params.update(extra_params)
    query_string = "&".join(f"{k}={v}" for k, v in params.items() if v)
    url = f"{config.authorize_url}?{query_string}"
    return url, req.state


def exchange_code_for_tokens(
    config: OAuthConfig,
    authorization_code: str,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": authorization_code,
        "redirect_uri": config.redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(config.token_url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return TokenResponse(
        access_token=data.get("access_token", ""),
        id_token=data.get("id_token", ""),
        refresh_token=data.get("refresh_token", ""),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in", 0),
        scope=data.get("scope", ""),
    )


def fetch_user_info(
    config: OAuthConfig,
    access_token: str,
) -> UserProfile:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(config.userinfo_url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return UserProfile(
        sub=data.get("sub", ""),
        name=data.get("name", ""),
        email=data.get("email", ""),
        email_verified=data.get("email_verified", False),
        picture=data.get("picture", ""),
        nickname=data.get("nickname", ""),
        given_name=data.get("given_name", ""),
        family_name=data.get("family_name", ""),
        locale=data.get("locale", ""),
        zoneinfo=data.get("zoneinfo", ""),
        updated_at=data.get("updated_at", 0),
        identities=data.get("identities", []),
        raw_claims=data,
    )


def normalize_claims(profile: UserProfile, provider: str = "auth0") -> NormalizedClaims:
    provider_user_id = profile.sub
    if "|" in provider_user_id:
        parts = provider_user_id.split("|", 1)
        provider_user_id = parts[1] if len(parts) > 1 else provider_user_id

    display_name = profile.name or profile.nickname or profile.email
    first_name = profile.given_name or ""
    last_name = profile.family_name or ""

    if not first_name and " " in display_name:
        parts = display_name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

    extra = {
        k: v
        for k, v in profile.raw_claims.items()
        if k
        not in (
            "sub",
            "name",
            "email",
            "email_verified",
            "picture",
            "nickname",
            "given_name",
            "family_name",
            "locale",
            "zoneinfo",
            "updated_at",
            "identities",
        )
    }

    return NormalizedClaims(
        user_id=profile.sub,
        email=profile.email,
        email_verified=profile.email_verified,
        display_name=display_name,
        first_name=first_name,
        last_name=last_name,
        avatar_url=profile.picture,
        locale=profile.locale,
        provider=provider,
        provider_user_id=provider_user_id,
        extra_attributes=extra,
    )


def generate_pkce_pair() -> PkcePair:
    return PkcePair.generate()


def build_pkce_authorization_url(
    config: OAuthConfig,
    pkce: PkcePair,
    state: Optional[str] = None,
    connection: Optional[str] = None,
) -> Tuple[str, str]:
    url, state = build_authorization_url(
        config=config,
        state=state,
        code_challenge=pkce.code_challenge,
        code_challenge_method=pkce.code_challenge_method,
        connection=connection,
    )
    return url, state


def verify_token_signature_hint(id_token: str) -> bool:
    parts = id_token.split(".")
    return len(parts) == 3
