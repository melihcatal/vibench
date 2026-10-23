from identity_client import CognitoIdentityClient
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_session(refresh_token: str) -> dict:
    client = CognitoIdentityClient()
    request = RefreshSessionRequest(refresh_token=refresh_token)
    response = client.refresh_session(refresh_token=request.refresh_token)
    return RefreshSessionResponse(**response).dict()
