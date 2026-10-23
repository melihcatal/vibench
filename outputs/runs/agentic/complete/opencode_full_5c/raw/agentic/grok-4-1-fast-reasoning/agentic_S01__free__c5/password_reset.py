from supabase import Client
from identity_client import get_identity_client


def password_reset(email: str) -> dict:
    client: Client = get_identity_client()
    response = client.auth.reset_password_for_email(email)
    return dict(response)
