from supabase import Client
from identity_client import get_supabase_client
from identity_models import UserLogin, SessionResponse
from gotrue.types import AuthResponse

def email_password_login(login_data: UserLogin) -> SessionResponse:
    """
    Signs in a user with email and password using Supabase.
    """
    supabase: Client = get_supabase_client()

    try:
        res: AuthResponse = supabase.auth.sign_in_with_password({
            "email": login_data.email,
            "password": login_data.password,
        })
        
        if res.user is None or res.session is None:
             raise Exception("Login failed: No user or session returned.")

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
        print(f"An error occurred during login: {e}")
        raise
