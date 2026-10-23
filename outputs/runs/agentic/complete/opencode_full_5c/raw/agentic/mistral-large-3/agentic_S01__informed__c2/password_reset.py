import os
from identity_client import FirebaseIdentityClient
from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
    normalize_password_reset_response,
)


def password_reset(email: str) -> PasswordResetResponse:
    client = FirebaseIdentityClient()
    response = client.send_password_reset_email(email)
    return normalize_password_reset_response(response)
