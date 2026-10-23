import os
import secrets
import urllib.parse
from identity_models import OAuthConfig, AuthorizationRequest
from identity_client import load_oauth_config, build_authorization_url


def start_oauth_login(
    config: OAuthConfig | None = None,
    state: str | None = None,
    connection: str | None = None,
    prompt: str | None = None,
) -> dict:
    if config is None:
        config = load_oauth_config()

    if not config.domain:
        raise ValueError("AUTH0_DOMAIN environment variable is required")
    if not config.client_id:
        raise ValueError("AUTH0_CLIENT_ID environment variable is required")

    extra_params = {}
    if prompt:
        extra_params["prompt"] = prompt

    authorization_url, generated_state = build_authorization_url(
        config=config,
        state=state,
        connection=connection,
        extra_params=extra_params if extra_params else None,
    )

    return {
        "authorization_url": authorization_url,
        "state": generated_state,
        "client_id": config.client_id,
        "domain": config.domain,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "provider": "auth0",
    }


def build_login_redirect(
    config: OAuthConfig | None = None,
    state: str | None = None,
    connection: str | None = None,
) -> str:
    result = start_oauth_login(config=config, state=state, connection=connection)
    return result["authorization_url"]


if __name__ == "__main__":
    result = start_oauth_login()
    print(f"Authorization URL: {result['authorization_url']}")
    print(f"State: {result['state']}")
    print(f"Provider: {result['provider']}")
