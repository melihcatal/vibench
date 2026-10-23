from identity_client import AUTH0_CONNECTION, auth0_api, post_json
from identity_models import PasswordResetRequest


def password_reset(email: str):
    payload = PasswordResetRequest(email=email).normalized()
    payload["connection"] = AUTH0_CONNECTION
    return post_json(auth0_api("/dbconnections/change_password"), payload)
