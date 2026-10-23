import requests
from identity_client import load_identity_config
from identity_models import PasswordResetRequest, as_payload, normalize_email


def password_reset(email: str) -> dict:
    config = load_identity_config()
    req = PasswordResetRequest(email=normalize_email(email), connection=config.auth0_connection)
    payload = as_payload(req)
    payload.update({"client_id": config.auth0_client_id, "email": req.email, "connection": req.connection})
    response = requests.post(f"https://{config.auth0_domain}/dbconnections/change_password", json=payload, timeout=30)
    response.raise_for_status()
    return {"status": "started", "detail": response.text}
