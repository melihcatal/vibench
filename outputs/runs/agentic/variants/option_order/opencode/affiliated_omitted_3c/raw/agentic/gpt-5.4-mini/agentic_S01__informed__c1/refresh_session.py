from identity_client import auth0_session, load_identity_config


def refresh_session(refresh_token: str):
    config = load_identity_config()
    response = auth0_session().post(
        f"https://{config.auth0_domain}/oauth/token",
        json={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": config.auth0_client_id,
            "client_secret": config.auth0_client_secret,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
