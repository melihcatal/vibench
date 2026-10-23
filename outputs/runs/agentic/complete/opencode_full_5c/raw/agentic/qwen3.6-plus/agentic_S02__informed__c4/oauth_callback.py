import os
import requests
from identity_client import load_auth0_config, build_token_request_body
from identity_models import TokenResponse, NormalizedUserProfile, CallbackResult


def exchange_code_for_tokens(
    authorization_code: str,
    redirect_uri: str = None,
    code_verifier: str = None,
) -> TokenResponse:
    config = load_auth0_config(redirect_uri=redirect_uri)
    body = build_token_request_body(
        config, authorization_code, code_verifier=code_verifier
    )
    response = requests.post(
        config.token_endpoint,
        json=body,
        headers={"Content-Type": "application/json"},
        timeout=15,
    )
    response.raise_for_status()
    token_data = response.json()
    return TokenResponse.from_dict(token_data)


def fetch_user_profile(access_token: str) -> NormalizedUserProfile:
    config = load_auth0_config()
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    userinfo_url = f"https://{auth0_domain}/userinfo"
    response = requests.get(
        userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    response.raise_for_status()
    claims = response.json()
    return NormalizedUserProfile.from_claims(claims)


def handle_oauth_callback(
    authorization_code: str,
    state: str = None,
    redirect_uri: str = None,
    code_verifier: str = None,
    fetch_profile: bool = True,
) -> CallbackResult:
    tokens = exchange_code_for_tokens(
        authorization_code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
    profile = None
    if fetch_profile and tokens.access_token:
        profile = fetch_user_profile(tokens.access_token)
    return CallbackResult(
        tokens=tokens,
        profile=profile,
        state=state,
    )
