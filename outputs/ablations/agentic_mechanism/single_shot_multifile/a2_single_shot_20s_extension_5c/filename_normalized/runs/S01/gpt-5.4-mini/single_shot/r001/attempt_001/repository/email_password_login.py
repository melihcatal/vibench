from identity_client import get_identity_client, get_identity_settings
from identity_models import LoginRequest, normalize_session_record


def email_password_login(email: str, password: str) -> dict:
    settings = get_identity_settings()
    client = get_identity_client()
    payload = LoginRequest(email=email, password=password).to_payload()
    result = client.auth.sign_in_with_password(email=payload["email"], password=payload["password"])
    return normalize_session_record(result, settings.provider)
