from identity_client import get_stytch_client
from identity_models import PasswordResetRequest, PasswordResetStartResponse


def password_reset_start(request: PasswordResetRequest) -> PasswordResetStartResponse:
    client = get_stytch_client()
    result = client.email.passwords.reset_start(email=request.email)
    return PasswordResetStartResponse(
        reset_code_id=result.reset_code_id, expires_at=result.expires_at
    )
