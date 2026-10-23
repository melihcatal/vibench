from identity_client import get_supabase_client
from identity_models import normalize_email

def password_reset(email: str):
    client = get_supabase_client()
    client.auth.reset_password_for_email(normalize_email(email))
    return {"status": "reset_email_sent"}