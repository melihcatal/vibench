from identity_client import supabase_client
from identity_models import RefreshRequest, AuthResponse
from gotrue.errors import GoTrueApiError

def refresh_user_session(refresh_data: RefreshRequest) -> AuthResponse:
    """Refreshes a user session using a refresh token with Supabase Auth."""
    try:
        res = supabase_client.auth.refresh_session(refresh_data.refresh_token)
        
        if not res.user or not res.session:
             raise ValueError("Session refresh failed, no user or session returned.")

        return AuthResponse(
            access_token=res.session.access_token,
            refresh_token=res.session.refresh_token or refresh_data.refresh_token,
            user_id=str(res.user.id),
            expires_in=res.session.expires_in
        )
    except GoTrueApiError as e:
        raise ValueError(f"Supabase session refresh failed: {e.message}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during session refresh: {e}")
