import os
from supabase import create_client
from identity_client import get_supabase_config
from identity_models import parse_refresh_response


def refresh_session(refresh_token: str) -> dict:
    config = get_supabase_config()
    client = create_client(**config)
    response = client.auth.refresh_session(refresh_token=refresh_token)
    return parse_refresh_response(response)
