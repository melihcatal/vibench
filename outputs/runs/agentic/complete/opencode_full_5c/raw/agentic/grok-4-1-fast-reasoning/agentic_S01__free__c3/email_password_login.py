import os
from supabase import create_client
from identity_client import SUPABASE_URL, SUPABASE_ANON_KEY
from identity_models import LoginInput, AuthSession


def email_password_login(login_input: LoginInput) -> AuthSession:
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    response = supabase.auth.sign_in_with_password(dict(login_input))
    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user_id": response.user.id,
    }
