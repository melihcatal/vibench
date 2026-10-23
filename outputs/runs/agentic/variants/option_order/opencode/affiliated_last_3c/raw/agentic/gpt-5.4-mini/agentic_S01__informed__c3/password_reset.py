from identity_client import auth0_request
from identity_models import PasswordResetRequest


def password_reset(email: str) -> dict:
    payload = PasswordResetRequest(email=email).normalized()
    return auth0_request(
        "POST",
        "/dbconnections/change_password",
        json={"email": payload.email, "connection": "Username-Password-Authentication"},
    )
