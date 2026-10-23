import os
from supabase import create_client
from identity_client import get_supabase_config
from identity_models import parse_login_response


def email_password_login(email: str, password: str) -> dict:
    config = get_supabase_config()
    client = create_client(**config)
    response = client.auth.sign_in_with_password(email=email, password=password)
    return parse_login_response(response)
