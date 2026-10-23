from identity_client import auth0_base_url, get_session
from identity_models import PasswordResetRequest, normalize_email


def password_reset(email: str):
    req = PasswordResetRequest(email=normalize_email(email))
    session = get_session()
    response = session.post(
        f"{auth0_base_url()}/dbconnections/change_password",
        json={"email": req.email, "connection": "Username-Password-Authentication"},
        timeout=30,
    )
    response.raise_for_status()
    return response.text
