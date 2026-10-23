from identity_client import get_supabase_client
from identity_models import UserCredentials, Session
from gotrue.errors import GoTrueApiError

def login_with_email_password(credentials: UserCredentials) -> Session:
    """
    Signs in a user with their email and password using Supabase.
    """
    supabase = get_supabase_client()
    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        if response.session:
             return Session(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                token_type=response.session.token_type,
                expires_in=response.session.expires_in
            )
        else:
            raise Exception("Login failed: No session data in response.")

    except GoTrueApiError as e:
        raise Exception(f"API Error during login: {e.message}")
    except Exception as e:
        raise e
