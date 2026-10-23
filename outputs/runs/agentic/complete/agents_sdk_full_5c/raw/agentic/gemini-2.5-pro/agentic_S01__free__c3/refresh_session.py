from supabase import Client
from identity_client import get_supabase_client
from identity_models import RefreshRequest, SessionResponse
from gotrue.types import AuthResponse


def refresh_session(refresh_request: RefreshRequest) -> SessionResponse:
    """
    Refreshes an expired session using a refresh token with Supabase.
    """
    supabase: Client = get_supabase_client()
    
    try:
        res: AuthResponse = supabase.auth.refresh_session(refresh_request.refresh_token)
        
        if res.user is None or res.session is None:
             raise Exception("Refresh failed: No user or session returned.")
        
        user_profile = {
            "id": res.user.id,
            "email": res.user.email,
            "created_at": res.user.created_at.isoformat()
        }

        session_data = {
            "access_token": res.session.access_token,
            "token_type": res.session.token_type,
            "expires_in": res.session.expires_in,
            "refresh_token": res.session.refresh_token,
            "user": user_profile,
        }

        return SessionResponse(**session_data)

    except Exception as e:
        print(f"An error occurred during session refresh: {e}")
        raise
