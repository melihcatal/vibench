import os
import json
import time
from typing import Dict, Any, Optional

from identity_models import OAuthConfig, PKCEState
from identity_client import (
    get_oauth_config,
    start_login_flow,
    generate_state,
    generate_nonce,
    generate_code_verifier,
    generate_code_challenge,
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
)


def initiate_oauth_login(
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    config = get_oauth_config()

    if redirect_uri:
        config.redirect_uri = redirect_uri
    if scope:
        config.scope = scope
    if audience:
        config.audience = audience

    auth_url, session_data = start_login_flow(
        config=config,
        use_pkce=False,
        extra_params=extra_params,
    )

    result = {
        "authorization_url": auth_url,
        "state": session_data["state"],
        "nonce": session_data["nonce"],
        "provider": "auth0",
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
        "initiated_at": session_data["timestamp"],
    }

    return result


def initiate_pkce_login(
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    code_verifier: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    config = get_oauth_config()

    if redirect_uri:
        config.redirect_uri = redirect_uri
    if scope:
        config.scope = scope

    auth_url, session_data = start_login_flow(
        config=config,
        use_pkce=True,
        code_verifier=code_verifier,
        extra_params=extra_params,
    )

    result = {
        "authorization_url": auth_url,
        "state": session_data["state"],
        "nonce": session_data["nonce"],
        "code_verifier": session_data["pkce_state"]["code_verifier"],
        "code_challenge": session_data["pkce_state"]["code_challenge"],
        "code_challenge_method": session_data["pkce_state"]["code_challenge_method"],
        "provider": "auth0",
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
        "initiated_at": session_data["timestamp"],
    }

    return result


if __name__ == "__main__":
    result = initiate_oauth_login()
    print(json.dumps(result, indent=2))
