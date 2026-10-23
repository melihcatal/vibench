from identity_client import supabase_request
from identity_models import LoginRequest, normalize_supabase_auth_response


def email_password_login(email: str, password: str) -> dict:
    request = LoginRequest(email=email, password=password)
    payload = supabase_request(
        "POST",
        "/auth/v1/token?grant_type=password",
        request.to_supabase_payload(),
    )
    return normalize_supabase_auth_response(payload)
