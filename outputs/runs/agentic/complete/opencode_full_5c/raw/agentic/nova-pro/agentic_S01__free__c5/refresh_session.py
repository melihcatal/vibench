from identity_client import auth, translate_client
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_session(refresh_token: str) -> RefreshSessionResponse:
    custom_token = auth.verify_id_token(refresh_token)
    return RefreshSessionResponse(custom_token)
