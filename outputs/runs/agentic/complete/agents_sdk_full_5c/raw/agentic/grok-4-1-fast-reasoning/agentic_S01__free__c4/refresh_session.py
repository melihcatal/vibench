import os
from supabase import create_client, Client
from identity_client import get_supabase_client
from identity_models import normalize_tokens
from typing import Dict, Any

def refresh_session(refresh_token: str) -> Dict[str, Any]:
    client = get_supabase_client()
    response = client.auth.refresh_session(refresh_token)
    tokens = normalize_tokens(response)
    return {"tokens": tokens}