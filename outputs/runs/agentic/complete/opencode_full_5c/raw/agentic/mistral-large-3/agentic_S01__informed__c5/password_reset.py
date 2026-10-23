import os
from identity_client import IBMAppIDClient
from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
    normalize_password_reset_response,
)


def password_reset(email: str) -> PasswordResetResponse:
    client = IBMAppIDClient()
    return client.password_reset(PasswordResetRequest(email=email))
