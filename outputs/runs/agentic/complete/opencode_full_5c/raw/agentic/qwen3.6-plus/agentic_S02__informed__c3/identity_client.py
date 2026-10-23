import os
import secrets
import hashlib
import base64
import time
import uuid
from typing import Optional, Dict, Any, Tuple

import requests

from identity_models import (
    OAuthConfig,
    PKCEState,
    TokenResponse,
    UserProfile,
    build_authorization_url,
    build_token_request_payload,
    parse_token_response,
    normalize_profile_claims,
)


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.environ.get(
    "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
)
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "")


def get_oauth_config() -> OAuthConfig:
    return OAuthConfig(
        provider="auth0",
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        redirect_uri=AUTH0_REDIRECT_URI,
        audience=AUTH0_AUDIENCE,
    )


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def generate_nonce() -> str:
    return secrets.token_urlsafe(32)


def generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def create_pkce_state(code_verifier: Optional[str] = None) -> PKCEState:
    verifier = code_verifier or generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    state = generate_state()
    return PKCEState(
        code_verifier=verifier,
        code_challenge=challenge,
        code_challenge_method="S256",
        state=state,
    )


def start_login_flow(
    config: Optional[OAuthConfig] = None,
    use_pkce: bool = False,
    code_verifier: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> Tuple[str, Dict[str, Any]]:
    if config is None:
        config = get_oauth_config()

    state = generate_state()
    nonce = generate_nonce()

    pkce_state = None
    if use_pkce:
        pkce_state = create_pkce_state(code_verifier)
        state = pkce_state.state

    auth_url = build_authorization_url(
        config=config,
        state=state,
        nonce=nonce,
        pkce_state=pkce_state,
        extra_params=extra_params,
    )

    session_data = {
        "state": state,
        "nonce": nonce,
        "pkce_state": pkce_state.to_dict() if pkce_state else None,
        "timestamp": time.time(),
    }

    return auth_url, session_data


def exchange_code_for_tokens(
    code: str,
    config: Optional[OAuthConfig] = None,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    if config is None:
        config = get_oauth_config()

    payload = build_token_request_payload(config, code, code_verifier)

    response = requests.post(
        config.token_endpoint,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    response.raise_for_status()

    token_data = response.json()
    return parse_token_response(token_data)


def fetch_user_profile(
    access_token: str,
    config: Optional[OAuthConfig] = None,
) -> UserProfile:
    if config is None:
        config = get_oauth_config()

    response = requests.get(
        config.userinfo_endpoint,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()

    raw_claims = response.json()
    return normalize_profile_claims(raw_claims, provider="auth0")


def revoke_token(
    token: str,
    config: Optional[OAuthConfig] = None,
) -> bool:
    if config is None:
        config = get_oauth_config()

    revoke_url = f"https://{config.domain}/oauth/revoke"
    payload = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "token": token,
    }

    response = requests.post(
        revoke_url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    return response.status_code == 200


def generate_event_id() -> str:
    return str(uuid.uuid4())
