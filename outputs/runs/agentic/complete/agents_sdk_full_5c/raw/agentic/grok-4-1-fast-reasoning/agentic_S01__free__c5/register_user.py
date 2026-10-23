from identity_client import get_supabase_client
from identity_models import build_signup_payload

def register_user(email: str, password: str):
    client = get_supabase_client()
    payload = build_signup_payload(email, password)
    response = client.auth.sign_up(payload)
    return {
        "user_id": response.user.id,
        "email": response.user.email
    }