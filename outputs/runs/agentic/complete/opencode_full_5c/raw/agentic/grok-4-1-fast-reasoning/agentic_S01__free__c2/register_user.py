import os
from supabase import create_client
from identity_client import get_supabase_config
from identity_models import parse_signup_response


def register_user(email: str, password: str) -> dict:
    config = get_supabase_config()
    client = create_client(**config)
    response = client.auth.sign_up(email=email, password=password)
    return parse_signup_response(response)
