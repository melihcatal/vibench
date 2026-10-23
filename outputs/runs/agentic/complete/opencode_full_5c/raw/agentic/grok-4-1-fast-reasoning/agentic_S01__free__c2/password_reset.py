import os
from supabase import create_client
from identity_client import get_supabase_config


def password_reset(email: str) -> dict:
    config = get_supabase_config()
    client = create_client(**config)
    response = client.auth.reset_password_for_email(email=email)
    return {"status": "password_reset_email_sent"}
