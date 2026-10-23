from identity_client import get_identity_client
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_session(refresh_token: str | None = None, access_token: str | None = None) -> dict:
    client = get_identity_client()
    req = RefreshSessionRequest(refresh_token=refresh_token, access_token=access_token)
    session = client.refresh_session(req)
    return RefreshSessionResponse.from_session(session).to_dict()
