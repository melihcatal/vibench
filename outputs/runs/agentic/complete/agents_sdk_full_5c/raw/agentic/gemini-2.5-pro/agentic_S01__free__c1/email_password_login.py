from identity_client import supabase_client
from identity_models import UserLogin, AuthResponse
from gotrue.errors import GoTrueApiError

def login_with_email_password(credentials: UserLogin) -> AuthResponse:
    """Signs in a user with email and password using Supabase Auth."""
    try:
        res = supabase_client.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        if not res.user or not res.session:
             raise ValueError("Login failed, no user or session returned.")

        return AuthResponse(
            access_token=res.session.access_token,
            refresh_token=res.session.refresh_token,
            user_id=str(res.user.id),
            expires_in=res.session.expires_in
        )
    except GoTrueApiError as e:
        raise ValueError(f"Supabase login failed: {e.message}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during login: {e}")
