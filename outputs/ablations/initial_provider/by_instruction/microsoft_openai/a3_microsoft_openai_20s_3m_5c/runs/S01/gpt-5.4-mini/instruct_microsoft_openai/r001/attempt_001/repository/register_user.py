from identity_client import load_identity_config, post_auth0
from identity_models import EmailPasswordRequest, normalize_email


def register_user(request: EmailPasswordRequest):
    config = load_identity_config()
    payload = {
        "email": normalize_email(request.email),
        "password": request.password,
        "connection": config.auth0_connection or "Username-Password-Authentication",
    }
    return post_auth0("/api/v2/users", payload, config=config)
