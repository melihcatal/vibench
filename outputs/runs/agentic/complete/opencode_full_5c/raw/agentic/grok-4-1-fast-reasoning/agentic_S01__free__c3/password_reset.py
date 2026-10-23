import os
from supabase import create_client
from identity_client import SUPABASE_URL, SUPABASE_ANON_KEY
from identity_models import PasswordResetInput
from typing import Dict, Any


def start_password_reset(reset_input: PasswordResetInput) -> Dict[str, Any]:
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    response = supabase.auth.reset_password_for_email(reset_input["email"])
    return {"status": "email_sent", "data": response}
