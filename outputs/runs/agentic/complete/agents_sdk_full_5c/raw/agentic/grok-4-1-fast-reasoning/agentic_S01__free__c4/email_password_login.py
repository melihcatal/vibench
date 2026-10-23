import os
from supabase import create_client, Client
from identity_client import get_supabase_client
from identity_models import LoginRequest, normalize_tokens
from typing import Dict, Any

def email_password_login(email: str, password: str) -> Dict[str, Any]:
    client = get_supabase_client()
    request: LoginRequest = {"email": email, "password": password}
    response = client.auth.sign_in_with_password(request)
    tokens = normalize_tokens(response)
    return {"tokens": tokens}