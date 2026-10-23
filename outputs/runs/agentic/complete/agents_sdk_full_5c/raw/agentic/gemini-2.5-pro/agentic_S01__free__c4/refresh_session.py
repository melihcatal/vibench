from identity_client import get_supabase_client
from identity_models import Session
from gotrue.errors import GoTrueApiError

def refresh_user_session(refresh_token: str) -> Session:
    """
    Refreshes a user session using a refresh token with Supabase.
    """
    supabase = get_supabase_client()
    try:
        response = supabase.auth.refresh_session(refresh_token)
        if response.session:
            return Session(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                token_type=response.session.token_type,
                expires_in=response.session.expires_in
            )
        else:
            raise Exception("Session refresh failed: No session data in response.")

    except GoTrueApiError as e:
        raise Exception(f"API Error during session refresh: {e.message}")
    except Exception as e:
        raise e
