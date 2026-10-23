import os
from supabase import create_client, Client
from identity_client import get_supabase_client
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_token: str) -> dict:
    """
    Refreshes an expired session or access token using Supabase Auth.
    """
    supabase = get_supabase_client()

    try:
        # Set the refresh token and refresh session
        supabase.auth.set_session(refresh_token)

        # Refresh the session
        auth_response = supabase.auth.refresh_session()

        user = auth_response.user
        session = auth_response.session

        if not user or not session:
            raise Exception("Session refresh failed")

        return {
            "user_id": user.id,
            "email": user.email,
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "expires_at": session.expires_at,
            "token_type": "bearer",
        }

    except Exception as e:
        print(f"Session refresh error: {e}")
        raise
