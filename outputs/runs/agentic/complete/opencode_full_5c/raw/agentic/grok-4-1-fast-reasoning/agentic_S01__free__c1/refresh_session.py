from identity_client import get_stytch_client
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(request: RefreshRequest) -> RefreshResponse:
    client = get_stytch_client()
    result = client.sessions.authenticate(request.session_token)
    session = result.session
    return RefreshResponse(
        session_token=session.session_token, session_jwt=session.session_jwt
    )
