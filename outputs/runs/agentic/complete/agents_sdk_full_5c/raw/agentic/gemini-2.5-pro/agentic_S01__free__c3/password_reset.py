from supabase import Client
from identity_client import get_supabase_client
from identity_models import PasswordResetRequest

def request_password_reset(reset_request: PasswordResetRequest) -> bool:
    """
    Starts a password reset flow for a user with Supabase.
    """
    supabase: Client = get_supabase_client()
    
    try:
        supabase.auth.reset_password_email(reset_request.email)
        # Supabase API for password reset does not return a detailed response on success,
        # it raises an error on failure.
        return True
    except Exception as e:
        print(f"An error occurred during password reset request: {e}")
        return False
