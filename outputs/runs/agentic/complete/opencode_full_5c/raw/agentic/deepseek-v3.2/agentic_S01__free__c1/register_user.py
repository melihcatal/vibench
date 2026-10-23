import os
from supabase import create_client, Client
from identity_client import get_supabase_client
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(email: str, password: str, display_name: str = None) -> dict:
    """
    Creates a new email/password user account using Supabase Auth.
    """
    supabase = get_supabase_client()

    try:
        # Create user with Supabase Auth
        auth_response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {
                    "data": {"display_name": display_name or email.split("@")[0]}
                },
            }
        )

        user = auth_response.user
        session = auth_response.session

        if not user:
            raise Exception("User registration failed")

        # Create user profile in public.users table
        profile_data = {
            "id": user.id,
            "email": user.email,
            "display_name": display_name or email.split("@")[0],
            "created_at": user.created_at,
        }

        supabase.table("users").insert(profile_data).execute()

        return {
            "user_id": user.id,
            "email": user.email,
            "session_token": session.access_token if session else None,
            "refresh_token": session.refresh_token if session else None,
            "display_name": display_name or email.split("@")[0],
        }

    except Exception as e:
        print(f"Registration error: {e}")
        raise
