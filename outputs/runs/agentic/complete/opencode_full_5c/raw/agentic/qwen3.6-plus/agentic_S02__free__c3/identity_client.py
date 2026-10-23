import os
import json
import time
from typing import Any, Dict, Optional

import requests

from identity_models import (
    OAuthConfig,
    PKCEConfig,
    AuthRequest,
    TokenResponse,
    UserProfile,
    generate_state,
    generate_nonce,
    generate_code_verifier,
    generate_code_challenge,
    decode_id_token_payload,
)


def load_oauth_config() -> OAuthConfig:
    issuer = os.environ.get("AUTH0_ISSUER", "https://dev-example.auth0.com")
    return OAuthConfig(
        issuer=issuer,
        authorization_endpoint=f"{issuer}/authorize",
        token_endpoint=f"{issuer}/oauth/token",
        userinfo_endpoint=f"{issuer}/userinfo",
        client_id=os.environ.get("AUTH0_CLIENT_ID", ""),
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET", ""),
        redirect_uri=os.environ.get(
            "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
        ),
        scopes=os.environ.get("AUTH0_SCOPES", "openid profile email").split(),
    )


def load_okta_config() -> OAuthConfig:
    org_url = os.environ.get("OKTA_ORG_URL", "https://dev-example.okta.com")
    return OAuthConfig(
        issuer=f"{org_url}/oauth2/default",
        authorization_endpoint=f"{org_url}/oauth2/default/v1/authorize",
        token_endpoint=f"{org_url}/oauth2/default/v1/token",
        userinfo_endpoint=f"{org_url}/oauth2/default/v1/userinfo",
        client_id=os.environ.get("OKTA_CLIENT_ID", ""),
        client_secret=os.environ.get("OKTA_CLIENT_SECRET", ""),
        redirect_uri=os.environ.get(
            "OKTA_REDIRECT_URI", "http://localhost:3000/callback"
        ),
        scopes=os.environ.get("OKTA_SCOPES", "openid profile email").split(),
    )


def build_auth_url(
    config: OAuthConfig,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None,
    prompt: Optional[str] = None,
    login_hint: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> str:
    request = AuthRequest(
        client_id=config.client_id,
        redirect_uri=config.redirect_uri,
        scope=" ".join(config.scopes),
        response_type=config.response_type,
        state=state or generate_state(),
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        nonce=nonce or generate_nonce(),
        prompt=prompt,
        login_hint=login_hint,
        extra_params=extra_params or {},
    )
    params = request.to_query_params()
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{config.authorization_endpoint}?{query}"


def exchange_code_for_tokens(
    config: OAuthConfig,
    authorization_code: str,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": config.redirect_uri,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
    }
    if code_verifier:
        token_data["code_verifier"] = code_verifier

    response = requests.post(
        config.token_endpoint,
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    token_json = response.json()

    return TokenResponse(
        access_token=token_json["access_token"],
        token_type=token_json.get("token_type", "Bearer"),
        expires_in=token_json.get("expires_in", 3600),
        refresh_token=token_json.get("refresh_token"),
        id_token=token_json.get("id_token"),
        scope=token_json.get("scope"),
    )


def fetch_user_profile(
    config: OAuthConfig,
    access_token: str,
) -> UserProfile:
    response = requests.get(
        config.userinfo_endpoint,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    claims = response.json()

    return UserProfile(
        sub=claims.get("sub", ""),
        email=claims.get("email"),
        email_verified=claims.get("email_verified", False),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        phone_number=claims.get("phone_number"),
        phone_verified=claims.get("phone_number_verified", False),
        preferred_username=claims.get("preferred_username"),
        updated_at=claims.get("updated_at"),
        raw_claims=claims,
    )


def fetch_profile_from_id_token(id_token: str) -> UserProfile:
    claims = decode_id_token_payload(id_token)
    return UserProfile(
        sub=claims.get("sub", ""),
        email=claims.get("email"),
        email_verified=claims.get("email_verified", False),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        phone_number=claims.get("phone_number"),
        phone_verified=claims.get("phone_number_verified", False),
        preferred_username=claims.get("preferred_username"),
        updated_at=claims.get("updated_at"),
        raw_claims=claims,
    )


def refresh_access_token(
    config: OAuthConfig,
    refresh_token: str,
) -> TokenResponse:
    response = requests.post(
        config.token_endpoint,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": config.client_id,
            "client_secret": config.client_secret,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    token_json = response.json()

    return TokenResponse(
        access_token=token_json["access_token"],
        token_type=token_json.get("token_type", "Bearer"),
        expires_in=token_json.get("expires_in", 3600),
        refresh_token=token_json.get("refresh_token", refresh_token),
        id_token=token_json.get("id_token"),
        scope=token_json.get("scope"),
    )


def validate_state(stored_state: str, received_state: str) -> bool:
    return stored_state == received_state


def extract_provider_from_issuer(issuer: str) -> str:
    if "auth0.com" in issuer:
        return "auth0"
    if "okta.com" in issuer:
        return "okta"
    if "accounts.google.com" in issuer:
        return "google"
    if "login.microsoftonline.com" in issuer:
        return "microsoft"
    if "facebook.com" in issuer:
        return "facebook"
    return issuer
