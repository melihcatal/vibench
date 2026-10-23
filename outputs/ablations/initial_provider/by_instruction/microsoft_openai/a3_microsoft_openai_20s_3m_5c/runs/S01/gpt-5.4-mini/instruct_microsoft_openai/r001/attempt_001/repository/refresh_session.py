from identity_client import load_identity_config, post_auth0


def refresh_session(refresh_token: str):
    config = load_identity_config()
    payload = {
        "grant_type": "refresh_token",
        "client_id": config.auth0_client_id,
        "refresh_token": refresh_token,
    }
    if config.auth0_client_secret:
        payload["client_secret"] = config.auth0_client_secret
    if config.auth0_audience:
        payload["audience"] = config.auth0_audience
    return post_auth0("/oauth/token", payload, config=config)
