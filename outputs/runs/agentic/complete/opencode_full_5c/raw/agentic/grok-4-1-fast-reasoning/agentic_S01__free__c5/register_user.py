from supabase import Client
from identity_client import get_identity_client


def register_user(email: str, password: str) -> dict:
    client: Client = get_identity_client()
    response = client.auth.sign_up({"email": email, "password": password})
    return dict(response)
