from identity_client import get_supabase_client
from identity_models import build_login_payload

def email_password_login(email: str, password: str):
    client = get_supabase_client()
    return client.auth.sign_in_with_password(build_login_payload(email, password))