import os
from supabase import create_client
from identity_client import SUPABASE_URL, SUPABASE_ANON_KEY
from identity_models import RefreshInput, AuthSession


def refresh_session(refresh_input: RefreshInput) -> AuthSession:
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    response = supabase.auth.refresh_session(dict(refresh_input))
    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user_id": response.user.id,
    }
