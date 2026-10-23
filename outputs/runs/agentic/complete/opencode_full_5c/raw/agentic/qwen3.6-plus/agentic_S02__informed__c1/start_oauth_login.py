import os
import secrets
from urllib.parse import urlencode

from identity_models import OAuthConfig
from identity_client import load_oauth_config, build_auth_url


def start_oauth_login(
    redirect_uri: str = None,
    scope: str = None,
    audience: str = None,
    connection: str = None,
    prompt: str = None,
    max_age: int = None,
    extra_params: dict = None,
) -> dict:
    config = load_oauth_config(
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
    )

    login_state = config.state
    login_nonce = config.nonce

    auth_url = build_auth_url(
        config=config,
        connection=connection,
        prompt=prompt,
        max_age=max_age,
        extra_params=extra_params,
    )

    return {
        "authorization_url": auth_url,
        "state": login_state,
        "nonce": login_nonce,
        "provider": "auth0",
        "domain": config.domain,
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
    }


def generate_login_redirect(
    redirect_uri: str = None,
    scope: str = None,
    audience: str = None,
    connection: str = None,
) -> str:
    result = start_oauth_login(
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
        connection=connection,
    )
    return result["authorization_url"]


def build_login_context(
    redirect_uri: str = None,
    scope: str = None,
    audience: str = None,
    connection: str = None,
    prompt: str = None,
    max_age: int = None,
) -> dict:
    result = start_oauth_login(
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
        connection=connection,
        prompt=prompt,
        max_age=max_age,
    )
    return {
        "auth0_domain": result["domain"],
        "auth0_client_id": result["client_id"],
        "authorization_url": result["authorization_url"],
        "state": result["state"],
        "nonce": result["nonce"],
        "provider": "auth0",
    }
