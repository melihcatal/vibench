from identity_client import get_identity_client, get_identity_settings
from identity_models import RefreshSessionRequest, normalize_session_record


def refresh_session(refresh_token: str) -> dict:
    settings = get_identity_settings()
    client = get_identity_client()
    payload = RefreshSessionRequest(refresh_token=refresh_token).to_payload()
    result = client.auth.refresh_session(refresh_token=payload["refresh_token"])
    return normalize_session_record(result, settings.provider)
