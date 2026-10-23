import os
import requests
from identity_client import (
    load_auth0_config,
    generate_state,
    generate_nonce,
    build_authorization_url,
)
from identity_models import AuthorizationRequest


def start_oauth_login(
    redirect_uri: str = None,
    scopes: list = None,
    prompt: str = None,
    acr_values: str = None,
) -> dict:
    config = load_auth0_config(redirect_uri=redirect_uri, scopes=scopes)
    state = generate_state()
    nonce = generate_nonce()
    authorization_url = build_authorization_url(config, state, nonce, prompt=prompt)
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    discovery_url = f"https://{auth0_domain}/.well-known/openid-configuration"
    well_known = requests.get(discovery_url, timeout=10).json()
    return {
        "authorization_url": authorization_url,
        "state": state,
        "nonce": nonce,
        "provider": "auth0",
        "auth0_domain": auth0_domain,
        "issuer": config.issuer,
        "authorization_endpoint": config.authorization_endpoint,
        "scopes": config.scopes,
        "well_known_endpoints": {
            "token_endpoint": well_known.get("token_endpoint"),
            "userinfo_endpoint": well_known.get("userinfo_endpoint"),
            "jwks_uri": well_known.get("jwks_uri"),
        },
    }


def create_authorization_request(
    redirect_uri: str = None,
    scopes: list = None,
    state: str = None,
    nonce: str = None,
    prompt: str = None,
) -> AuthorizationRequest:
    config = load_auth0_config(redirect_uri=redirect_uri, scopes=scopes)
    return AuthorizationRequest(
        client_id=config.client_id,
        redirect_uri=config.redirect_uri,
        scope=" ".join(config.scopes),
        response_type="code",
        state=state or generate_state(),
        nonce=nonce or generate_nonce(),
        prompt=prompt,
    )
