from identity_client import get_firebase_client
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_user_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    auth = get_firebase_client()
    try:
        refreshed_session = auth.refresh(request.refresh_token)
        return RefreshSessionResponse.parse_obj(refreshed_session)
    except Exception as e:
        raise e
