import os
from supabase import create_client, Client
from identity_client import get_supabase_client
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> dict:
    """
    Signs in a user with email and password and returns tokens using Supabase Auth.
    """
    supabase = get_supabase_client()

    try:
        # Sign in with email and password
        auth_response = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )

        user = auth_response.user
        session = auth_response.session

        if not user or not session:
            raise Exception("Login failed")

        # Get user profile from public.users table
        profile_response = (
            supabase.table("users").select("*").eq("id", user.id).execute()
        )
        profile = profile_response.data[0] if profile_response.data else {}

        return {
            "user_id": user.id,
            "email": user.email,
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "expires_at": session.expires_at,
            "display_name": profile.get("display_name", user.email.split("@")[0]),
            "profile_data": profile,
        }

    except Exception as e:
        print(f"Login error: {e}")
        raise
