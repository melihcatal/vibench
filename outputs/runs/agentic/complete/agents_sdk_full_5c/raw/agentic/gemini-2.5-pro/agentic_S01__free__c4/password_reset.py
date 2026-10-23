from pydantic import EmailStr
from identity_client import get_supabase_client
from gotrue.errors import GoTrueApiError

def send_password_reset_email(email: EmailStr) -> dict:
    """
    Initiates the password reset flow for a user via Supabase.
    """
    supabase = get_supabase_client()
    try:
        # Supabase returns an empty dict on success
        supabase.auth.reset_password_for_email(email)
        return {"message": "Password reset email sent successfully."}
    except GoTrueApiError as e:
        raise Exception(f"API Error during password reset: {e.message}")
    except Exception as e:
        raise e
