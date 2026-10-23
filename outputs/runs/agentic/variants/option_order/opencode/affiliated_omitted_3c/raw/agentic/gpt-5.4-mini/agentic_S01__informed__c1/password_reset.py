from identity_client import auth0_session, load_identity_config
from identity_models import ResetRequest


def password_reset(email: str):
    config = load_identity_config()
    request = ResetRequest(email=email)
    response = auth0_session().post(
        f"https://{config.auth0_domain}/dbconnections/change_password",
        json={
            "client_id": config.auth0_client_id,
            "email": request.payload()["email"],
            "connection": "Username-Password-Authentication",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.text
