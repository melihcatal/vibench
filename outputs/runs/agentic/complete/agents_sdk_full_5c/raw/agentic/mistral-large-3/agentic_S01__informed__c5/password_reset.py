import os
from identity_client import get_auth0_management_client
from identity_models import PasswordResetRequest, PasswordResetResponse

def start_password_reset(email: str) -> PasswordResetResponse:
    client = get_auth0_management_client()
    
    client.jobs.send_verification_email({
        "email": email,
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "connection": "Username-Password-Authentication"
    })
    
    return PasswordResetResponse(
        success=True,
        message="Password reset email sent"
    )