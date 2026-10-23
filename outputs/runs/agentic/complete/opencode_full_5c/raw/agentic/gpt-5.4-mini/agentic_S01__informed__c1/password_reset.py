from identity_client import AUTH0_CLIENT_ID, AUTH0_CONNECTION, auth0_json_post
from identity_models import normalize_email


def password_reset(email: str) -> dict:
    return auth0_json_post(
        "/dbconnections/change_password",
        {
            "client_id": AUTH0_CLIENT_ID,
            "email": normalize_email(email),
            "connection": AUTH0_CONNECTION,
        },
    )
