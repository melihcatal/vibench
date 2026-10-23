from identity_client import get_identity_client, normalize_email
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> dict:
    client = get_identity_client()
    req = PasswordResetRequest(email=normalize_email(email))
    result = client.start_password_reset(req)
    return PasswordResetResponse.from_result(result).to_dict()
