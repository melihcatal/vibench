import os
from identity_client import get_identity_client
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> PasswordResetResponse:
    client = get_identity_client()
    
    client.forgot_password(
        ClientId=os.getenv("AWS_COGNITO_CLIENT_ID"),
        Username=email
    )
    
    return PasswordResetResponse(
        is_success=True,
        message="Password reset initiated"
    )