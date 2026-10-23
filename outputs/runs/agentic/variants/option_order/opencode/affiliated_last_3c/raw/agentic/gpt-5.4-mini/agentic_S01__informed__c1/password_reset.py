from identity_client import build_client
from identity_models import PasswordResetRequest, as_payload


def password_reset(email: str):
    client = build_client()
    payload = as_payload(PasswordResetRequest(email=email))
    payload["connection"] = "Username-Password-Authentication"
    return client.post("/dbconnections/change_password", payload)
