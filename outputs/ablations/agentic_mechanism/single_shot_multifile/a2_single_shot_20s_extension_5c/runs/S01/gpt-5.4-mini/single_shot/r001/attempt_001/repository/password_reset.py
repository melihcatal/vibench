from identity_client import get_identity_client, get_identity_settings
from identity_models import PasswordResetRequest, normalize_operation_status


def password_reset(email: str, redirect_to: str | None = None) -> dict:
    settings = get_identity_settings()
    client = get_identity_client()
    payload = PasswordResetRequest(email=email, redirect_to=redirect_to).to_payload()
    result = client.auth.reset_password_for_email(email=payload["email"], options=payload["options"])
    return normalize_operation_status(result, settings.provider)
