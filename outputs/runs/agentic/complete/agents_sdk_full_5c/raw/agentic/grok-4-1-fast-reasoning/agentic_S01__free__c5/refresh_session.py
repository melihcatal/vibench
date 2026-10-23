from identity_client import get_supabase_client
from identity_models import extract_tokens

def refresh_session(refresh_token: str):
    client = get_supabase_client()
    response = client.auth.refresh_session(refresh_token)
    return extract_tokens(response.session)