import os
from supabase import create_client, Client
from identity_models import LoginRequest, LoginResponse
from identity_client import get_identity_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def email_password_login(request: LoginRequest) -> LoginResponse:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Sign in with email and password
    auth_response = supabase.auth.sign_in_with_password({
        "email": request.email,
        "password": request.password,
    })
    
    if auth_response.session is None:
        raise ValueError("Login failed")
    
    return LoginResponse(
        access_token=auth_response.session.access_token,
        refresh_token=auth_response.session.refresh_token,
        expires_at=auth_response.session.expires_at,
        user_id=auth_response.user.id,
    )