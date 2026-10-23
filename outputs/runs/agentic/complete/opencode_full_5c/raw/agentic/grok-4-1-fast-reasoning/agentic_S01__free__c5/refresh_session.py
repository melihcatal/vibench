from supabase import Client
from identity_client import get_identity_client


def refresh_session(refresh_token: str) -> dict:
    client: Client = get_identity_client()
    response = client.auth.refresh_session({"refresh_token": refresh_token})
    return dict(response)
