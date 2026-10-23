from supabase import Client
from identity_client import get_identity_client


def email_password_login(email: str, password: str) -> dict:
    client: Client = get_identity_client()
    response = client.auth.sign_in_with_password({"email": email, "password": password})
    return dict(response)
