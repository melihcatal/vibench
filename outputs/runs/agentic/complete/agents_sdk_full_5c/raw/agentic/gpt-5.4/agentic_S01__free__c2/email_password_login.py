from __future__ import annotations

from identity_client import get_supabase_client
from identity_models import LoginRequest, normalize_email, normalize_supabase_tokens


def email_password_login(request: LoginRequest):
    client = get_supabase_client()
    session = client.auth.sign_in_with_password(
        {
            "email": normalize_email(request.email),
            "password": request.password,
        }
    )
    payload = {
        "access_token": session.session.access_token,
        "refresh_token": session.session.refresh_token,
        "token_type": session.session.token_type,
        "expires_in": session.session.expires_in,
        "id_token": getattr(session.session, "id_token", None),
    }
    return normalize_supabase_tokens(payload)
