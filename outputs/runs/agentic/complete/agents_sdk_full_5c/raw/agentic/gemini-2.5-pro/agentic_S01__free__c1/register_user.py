from identity_client import supabase_client
from identity_models import UserRegistration, AuthResponse
from gotrue.errors import GoTrueApiError

def register_new_user(user_data: UserRegistration) -> AuthResponse:
    """Creates a new user account using Supabase Auth."""
    try:
        res = supabase_client.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "full_name": user_data.full_name
                }
            }
        })
        if not res.user or not res.session:
             raise ValueError("Registration failed, no user or session returned.")

        return AuthResponse(
            access_token=res.session.access_token,
            refresh_token=res.session.refresh_token,
            user_id=str(res.user.id),
            expires_in=res.session.expires_in
        )
    except GoTrueApiError as e:
        raise ValueError(f"Supabase registration failed: {e.message}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during registration: {e}")
