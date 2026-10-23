import secrets

from identity_client import build_authorization_url, load_identity_provider_config


def start_oauth_login() -> dict:
    config = load_identity_provider_config("OIDC")
    state = secrets.token_urlsafe(32)
    authorization_url, returned_state = build_authorization_url(config, state)
    return {
        "authorization_url": authorization_url,
        "state": returned_state,
        "issuer": config.issuer,
    }
