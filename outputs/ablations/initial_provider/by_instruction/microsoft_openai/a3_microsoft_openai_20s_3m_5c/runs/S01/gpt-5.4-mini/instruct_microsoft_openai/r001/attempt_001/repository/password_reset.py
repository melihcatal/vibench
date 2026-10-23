from identity_client import load_identity_config, post_auth0
from identity_models import normalize_email


def password_reset(email: str):
    config = load_identity_config()
    payload = {
        "client_id": config.auth0_client_id,
        "email": normalize_email(email),
        "connection": config.auth0_connection or "Username-Password-Authentication",
    }
    return post_auth0("/dbconnections/change_password", payload, config=config)
