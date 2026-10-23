from identity_client import get_supabase_client
from identity_models import UserCredentials, UserRegistrationResponse
from gotrue.errors import GoTrueApiError

def register_new_user(credentials: UserCredentials) -> UserRegistrationResponse:
    """
    Creates a new user in Supabase.
    """
    supabase = get_supabase_client()
    try:
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password,
        })
        if response.user:
            return UserRegistrationResponse(id=response.user.id, email=response.user.email)
        else:
            raise Exception("User registration failed: No user data in response.")

    except GoTrueApiError as e:
        raise Exception(f"API Error during registration: {e.message}")
    except Exception as e:
        raise e
