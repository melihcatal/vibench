from identity_client import supabase_request
from identity_models import RegisterUserRequest, normalize_supabase_auth_response


def register_user(email: str, password: str, display_name: str | None = None) -> dict:
    request = RegisterUserRequest(
        email=email, password=password, display_name=display_name
    )
    payload = supabase_request("POST", "/auth/v1/signup", request.to_supabase_payload())
    return normalize_supabase_auth_response(payload)
