from identity_client import get_supabase_client
from identity_models import build_refresh_payload

def refresh_session(refresh_token: str):
    client = get_supabase_client()
    return client.auth.refresh_session(build_refresh_payload(refresh_token))