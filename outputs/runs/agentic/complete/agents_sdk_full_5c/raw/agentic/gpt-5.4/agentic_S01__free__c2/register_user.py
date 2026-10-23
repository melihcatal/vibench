from __future__ import annotations

from identity_client import get_supabase_client
from identity_models import RegisterUserRequest, normalize_email, normalize_supabase_user


def register_user(request: RegisterUserRequest):
    client = get_supabase_client()
    response = client.auth.sign_up(
        {
            "email": normalize_email(request.email),
            "password": request.password,
            "options": {
                "data": {"display_name": request.display_name} if request.display_name else {}
            },
        }
    )
    user_payload = {
        "id": response.user.id,
        "email": response.user.email,
        "email_confirmed_at": getattr(response.user, "email_confirmed_at", None),
        "user_metadata": getattr(response.user, "user_metadata", {}) or {},
    }
    return normalize_supabase_user(user_payload)
