import os
import requests
from identity_client import (
    load_auth0_config,
    generate_state,
    generate_nonce,
    generate_pkce_pair,
    build_authorization_url,
    build_token_request_body,
)
from identity_models import TokenResponse, NormalizedUserProfile, PKCEPair


def initiate_pkce_login(
    redirect_uri: str = None,
    scopes: list = None,
) -> dict:
    config = load_auth0_config(redirect_uri=redirect_uri, scopes=scopes)
    state = generate_state()
    nonce = generate_nonce()
    pkce = generate_pkce_pair()
    authorization_url = build_authorization_url(config, state, nonce, pkce=pkce)
    return {
        "authorization_url": authorization_url,
        "state": state,
        "nonce": nonce,
        "code_verifier": pkce.code_verifier,
        "code_challenge": pkce.code_challenge,
        "code_challenge_method": pkce.code_challenge_method,
        "provider": "auth0",
        "auth0_domain": os.environ.get("AUTH0_DOMAIN", ""),
    }


def complete_pkce_login(
    authorization_code: str,
    code_verifier: str,
    redirect_uri: str = None,
    fetch_profile: bool = True,
) -> dict:
    config = load_auth0_config(redirect_uri=redirect_uri)
    body = build_token_request_body(
        config, authorization_code, code_verifier=code_verifier
    )
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    token_url = f"https://{auth0_domain}/oauth/token"
    response = requests.post(
        token_url,
        json=body,
        headers={"Content-Type": "application/json"},
        timeout=15,
    )
    response.raise_for_status()
    token_data = response.json()
    tokens = TokenResponse.from_dict(token_data)
    profile = None
    if fetch_profile and tokens.access_token:
        userinfo_url = f"https://{auth0_domain}/userinfo"
        userinfo_response = requests.get(
            userinfo_url,
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            timeout=10,
        )
        userinfo_response.raise_for_status()
        profile = NormalizedUserProfile.from_claims(userinfo_response.json())
    return {
        "tokens": tokens,
        "profile": profile,
        "provider": "auth0",
        "auth0_domain": auth0_domain,
    }


def full_pkce_flow(
    redirect_uri: str = None,
    scopes: list = None,
) -> dict:
    initiation = initiate_pkce_login(redirect_uri=redirect_uri, scopes=scopes)
    return {
        "step": "initiate_pkce",
        "authorization_url": initiation["authorization_url"],
        "state": initiation["state"],
        "code_verifier": initiation["code_verifier"],
        "provider": "auth0",
        "auth0_domain": initiation["auth0_domain"],
    }
