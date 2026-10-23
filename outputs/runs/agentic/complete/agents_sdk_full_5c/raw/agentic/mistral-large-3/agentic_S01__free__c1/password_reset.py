import os
from supabase import create_client, Client
from identity_models import PasswordResetRequest, PasswordResetResponse
from identity_client import get_identity_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def start_password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Trigger password reset email
    response = supabase.auth.reset_password_email(request.email)
    
    if response.error:
        raise ValueError(f"Password reset failed: {response.error.message}")
    
    return PasswordResetResponse(
        success=True,
        message="Password reset email sent",
    )