import os
from supabase import create_client, Client
from identity_models import RefreshSessionRequest, RefreshSessionResponse
from identity_client import get_identity_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Refresh the session using the refresh token
    auth_response = supabase.auth.refresh_session(request.refresh_token)
    
    if auth_response.session is None:
        raise ValueError("Session refresh failed")
    
    return RefreshSessionResponse(
        access_token=auth_response.session.access_token,
        refresh_token=auth_response.session.refresh_token,
        expires_at=auth_response.session.expires_at,
    )