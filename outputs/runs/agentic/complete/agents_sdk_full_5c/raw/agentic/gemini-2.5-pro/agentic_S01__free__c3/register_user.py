from supabase import Client
from identity_client import get_supabase_client
from identity_models import UserRegistration, SessionResponse
from gotrue.types import UserResponse

def register_user(user_data: UserRegistration) -> SessionResponse:
    """
    Creates a new email/password user account using Supabase.
    """
    supabase: Client = get_supabase_client()
    
    try:
        res: UserResponse = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
        })

        if res.user is None or res.session is None:
             raise Exception("Registration failed: No user or session returned.")

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
        # In a real app, handle different exceptions (e.g., user already exists)
        print(f"An error occurred during registration: {e}")
        raise
