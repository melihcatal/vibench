from identity_client import load_identity_config, post_auth0
from identity_models import EmailPasswordRequest, normalize_email


def email_password_login(request: EmailPasswordRequest):
    config = load_identity_config()
    payload = {
        "grant_type": "password",
        "username": normalize_email(request.email),
        "password": request.password,
        "client_id": config.auth0_client_id,
        "scope": "openid profile email offline_access",
    }
    if config.auth0_client_secret:
        payload["client_secret"] = config.auth0_client_secret
    if config.auth0_audience:
        payload["audience"] = config.auth0_audience
    return post_auth0("/oauth/token", payload, config=config)
