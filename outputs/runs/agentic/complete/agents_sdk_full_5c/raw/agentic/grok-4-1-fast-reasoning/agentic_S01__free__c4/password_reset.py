import os
from supabase import create_client, Client
from identity_client import get_supabase_client
from typing import Dict, Any

def password_reset(email: str) -> Dict[str, Any]:
    client = get_supabase_client()
    client.auth.reset_password_for_email(email)
    return {"status": "password_reset_email_sent"}