from __future__ import annotations

from identity_client import get_supabase_client
from identity_models import PasswordResetRequest, normalize_email


def password_reset(request: PasswordResetRequest):
    client = get_supabase_client()
    client.auth.reset_password_email(normalize_email(request.email))
    return {"email": normalize_email(request.email), "status": "reset_requested", "provider": "supabase"}
