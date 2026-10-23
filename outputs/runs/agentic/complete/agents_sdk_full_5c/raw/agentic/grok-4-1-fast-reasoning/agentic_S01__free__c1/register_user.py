from identity_client import get_supabase_client
from identity_models import build_signup_payload

def register_user(email: str, password: str):
    client = get_supabase_client()
    return client.auth.sign_up(build_signup_payload(email, password))