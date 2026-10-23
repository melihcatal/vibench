from identity_models import RefreshSessionRequest, RefreshSessionResponse
from identity_client import IdentityClient

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    identity_client = IdentityClient()
    refresh_result = identity_client.refresh_session(request.refresh_token)

    return RefreshSessionResponse(
        access_token=refresh_result["access_token"],
        expires_in=refresh_result["expires_in"]
    )
