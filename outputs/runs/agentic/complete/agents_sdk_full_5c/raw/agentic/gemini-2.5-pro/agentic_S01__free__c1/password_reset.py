from identity_client import supabase_client
from identity_models import PasswordResetRequest
from gotrue.errors import GoTrueApiError

def request_password_reset(reset_request: PasswordResetRequest) -> bool:
    """
    Starts the password reset flow for a user via Supabase Auth.
    """
    try:
        # The Supabase client's reset_password_for_email does not return a value on success.
        # It raises a GoTrueApiError on failure (e.g., user not found).
        supabase_client.auth.reset_password_for_email(reset_request.email)
        return True
    except GoTrueApiError as e:
        # Log the error or handle it as needed; for security, often we don't
        # want to reveal if an email exists or not.
        print(f"Supabase password reset request failed: {e.message}")
        # Return True to prevent account enumeration attacks.
        return True
    except Exception as e:
        print(f"An unexpected error occurred during password reset request: {e}")
        # Depending on policy, you might still return True.
        return False
