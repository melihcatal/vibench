from identity_client import supabase_request
from identity_models import RefreshSessionRequest, normalize_session


def refresh_session(refresh_token: str) -> dict:
    request = RefreshSessionRequest(refresh_token=refresh_token)
    payload = supabase_request(
        "POST",
        "/auth/v1/token?grant_type=refresh_token",
        request.to_supabase_payload(),
    )
    return normalize_session(payload)
