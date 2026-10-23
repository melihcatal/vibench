import os
import base64
import hashlib
import secrets
from typing import Optional
from urllib.parse import urlencode

from identity_models import OAuthConfig, PKCEChallenge
from identity_client import load_oauth_config, build_auth_url


def generate_pkce_challenge(
    code_verifier: Optional[str] = None,
) -> PKCEChallenge:
    if code_verifier is None:
        code_verifier = secrets.token_urlsafe(64)

    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

    return PKCEChallenge(
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )


def start_pkce_login(
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    connection: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> dict:
    config = load_oauth_config(
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
    )

    pkce = generate_pkce_challenge(code_verifier)

    auth_url = build_auth_url(
        config=config,
        code_challenge=pkce.code_challenge,
        code_challenge_method=pkce.code_challenge_method,
        connection=connection,
    )

    return {
        "authorization_url": auth_url,
        "state": config.state,
        "nonce": config.nonce,
        "code_verifier": pkce.code_verifier,
        "code_challenge": pkce.code_challenge,
        "code_challenge_method": pkce.code_challenge_method,
        "provider": "auth0",
        "domain": config.domain,
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
    }


def complete_pkce_login(
    authorization_code: str,
    state: str,
    expected_state: str,
    code_verifier: str,
    redirect_uri: Optional[str] = None,
) -> dict:
    from oauth_callback import handle_oauth_callback

    return handle_oauth_callback(
        authorization_code=authorization_code,
        state=state,
        expected_state=expected_state,
        code_verifier=code_verifier,
        redirect_uri=redirect_uri,
    )


def build_pkce_auth_url(
    code_challenge: str,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    connection: Optional[str] = None,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
) -> str:
    config = load_oauth_config(
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
        state=state,
        nonce=nonce,
    )

    return build_auth_url(
        config=config,
        code_challenge=code_challenge,
        code_challenge_method="S256",
        connection=connection,
    )


def pkce_login_flow(
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    connection: Optional[str] = None,
) -> dict:
    login_init = start_pkce_login(
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
        connection=connection,
    )

    return {
        "step": "init",
        "authorization_url": login_init["authorization_url"],
        "state": login_init["state"],
        "nonce": login_init["nonce"],
        "code_verifier": login_init["code_verifier"],
        "provider": "auth0",
        "domain": login_init["domain"],
    }
