import os
from typing import Dict, Any
from identity_client import get_identity_client
from identity_models import PasswordResetRequest, PasswordResetResponse


def start_password_reset(email: str) -> PasswordResetResponse:
    client = get_identity_client()
    
    response = client.send_password_reset_email(
        email=email,
        redirect_url=os.getenv("AUTH0_PASSWORD_RESET_REDIRECT_URL")
    )
    
    return PasswordResetResponse(
        email_sent=response["email_sent"],
        reset_initiated=response["reset_initiated"]
    )