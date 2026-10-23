from identity_client import supabase_request
from identity_models import PasswordResetRequest


def password_reset(email: str, redirect_to: str | None = None) -> dict:
    request = PasswordResetRequest(email=email, redirect_to=redirect_to)
    payload = {"email": request.email}
    if request.redirect_to:
        payload["options"] = {"redirectTo": request.redirect_to}
    supabase_request("POST", "/auth/v1/recover", payload)
    return {"email": email, "reset_requested": True, "provider": "supabase"}
