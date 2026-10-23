from identity_client import get_supabase_client
from identity_models import normalize_email, extract_tokens

def email_password_login(email: str, password: str):
    client = get_supabase_client()
    response = client.auth.sign_in_with_password({
        "email": normalize_email(email),
        "password": password
    })
    return extract_tokens(response.session)