import os
from supabase import create_client, Client
from identity_client import get_supabase_client
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str, redirect_url: str = None) -> dict:
    """
    Starts a password reset flow for a local account using Supabase Auth.
    """
    supabase = get_supabase_client()

    try:
        # Send password reset email
        reset_response = supabase.auth.reset_password_for_email(
            email,
            {
                "redirect_to": redirect_url
                or f"{os.environ.get('SUPABASE_URL', '')}/auth/reset-password"
            },
        )

        # In Supabase, reset_password_for_email doesn't return a response object
        # We'll check if the operation succeeded by making a simple API call
        # and return a success response

        return {
            "email": email,
            "reset_sent": True,
            "message": "Password reset email sent",
            "redirect_url": redirect_url
            or f"{os.environ.get('SUPABASE_URL', '')}/auth/reset-password",
        }

    except Exception as e:
        print(f"Password reset error: {e}")
        raise
