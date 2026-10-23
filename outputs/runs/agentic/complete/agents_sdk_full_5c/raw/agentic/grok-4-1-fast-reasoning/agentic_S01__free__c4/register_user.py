import os
from supabase import create_client, Client
from identity_client import get_supabase_client
from identity_models import RegisterRequest
from typing import Dict, Any

def register_user(email: str, password: str) -> Dict[str, Any]:
    client: Client = get_supabase_client()
    request: RegisterRequest = {"email": email, "password": password}
    response = client.auth.sign_up(request)
    return response