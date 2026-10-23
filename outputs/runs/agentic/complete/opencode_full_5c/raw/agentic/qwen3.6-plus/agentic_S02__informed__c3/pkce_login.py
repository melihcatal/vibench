import os
import json
import time
import secrets
import hashlib
import base64
from typing import Dict, Any, Optional

import requests

from identity_models import OAuthConfig, PKCEState, TokenResponse, UserProfile
from identity_client import (
    get_oauth_config,
    generate_state,
    generate_nonce,
    generate_code_verifier,
    generate_code_challenge,
    create_pkce_state,
    exchange_code_for_tokens,
    fetch_user_profile,
    generate_event_id,
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
)


def generate_pkce_pair() -> Dict[str, str]:
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }


def build_pkce_authorization_url(
    code_challenge: str,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    config: Optional[OAuthConfig] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    if config is None:
        config = get_oauth_config()

    if state is None:
        state = generate_state()
    if nonce is None:
        nonce = generate_nonce()

    from identity_models import build_authorization_url

    pkce_state = PKCEState(
        code_verifier="",
        code_challenge=code_challenge,
        code_challenge_method="S256",
        state=state,
    )

    auth_url = build_authorization_url(
        config=config,
        state=state,
        nonce=nonce,
        pkce_state=pkce_state,
        extra_params=extra_params,
    )

    return {
        "authorization_url": auth_url,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "provider": "auth0",
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
    }


def complete_pkce_login(
    authorization_code: str,
    code_verifier: str,
    expected_state: Optional[str] = None,
    received_state: Optional[str] = None,
    config: Optional[OAuthConfig] = None,
) -> Dict[str, Any]:
    if config is None:
        config = get_oauth_config()

    if expected_state and received_state and expected_state != received_state:
        return {
            "success": False,
            "error": "state_mismatch",
            "message": "PKCE state parameter mismatch",
            "provider": "auth0",
        }

    try:
        token_response = exchange_code_for_tokens(
            code=authorization_code,
            config=config,
            code_verifier=code_verifier,
        )

        profile = None
        if token_response.access_token:
            try:
                profile = fetch_user_profile(token_response.access_token, config)
            except Exception:
                pass

        audit_event = {
            "event_id": generate_event_id(),
            "event_type": "pkce_login_complete",
            "timestamp": time.time(),
            "user_sub": profile.sub if profile else "",
            "provider": "auth0",
            "domain": AUTH0_DOMAIN,
            "client_id": AUTH0_CLIENT_ID,
            "success": True,
            "flow_type": "pkce",
        }

        return {
            "success": True,
            "tokens": token_response.to_dict(),
            "profile": profile.to_dict() if profile else None,
            "audit_event": audit_event,
            "provider": "auth0",
        }

    except Exception as e:
        audit_event = {
            "event_id": generate_event_id(),
            "event_type": "pkce_login_complete",
            "timestamp": time.time(),
            "provider": "auth0",
            "domain": AUTH0_DOMAIN,
            "client_id": AUTH0_CLIENT_ID,
            "success": False,
            "error": str(e),
            "flow_type": "pkce",
        }

        return {
            "success": False,
            "error": "pkce_token_exchange_failed",
            "message": str(e),
            "audit_event": audit_event,
            "provider": "auth0",
        }


def full_pkce_flow(
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
) -> Dict[str, Any]:
    config = get_oauth_config()

    if redirect_uri:
        config.redirect_uri = redirect_uri
    if scope:
        config.scope = scope

    pkce_pair = generate_pkce_pair()
    state = generate_state()
    nonce = generate_nonce()

    auth_url_result = build_pkce_authorization_url(
        code_challenge=pkce_pair["code_challenge"],
        state=state,
        nonce=nonce,
        config=config,
    )

    return {
        "step": "authorization_url_generated",
        "authorization_url": auth_url_result["authorization_url"],
        "state": state,
        "nonce": nonce,
        "code_verifier": pkce_pair["code_verifier"],
        "code_challenge": pkce_pair["code_challenge"],
        "provider": "auth0",
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
    }


if __name__ == "__main__":
    result = full_pkce_flow()
    print(json.dumps(result, indent=2))
