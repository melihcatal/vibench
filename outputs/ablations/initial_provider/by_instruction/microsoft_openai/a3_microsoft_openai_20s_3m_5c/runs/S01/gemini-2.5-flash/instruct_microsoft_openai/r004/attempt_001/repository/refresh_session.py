from identity_client import IdentityClient
from identity_models import RefreshTokenRequest, RefreshTokenResponse

def refresh_session(request: RefreshTokenRequest) -> RefreshTokenResponse:
    identity_client = IdentityClient()
    result = identity_client.refresh_token(request.refresh_token)
    if "access_token" in result:
        return RefreshTokenResponse(access_token=result["access_token"], message=result["message"])
    else:
        raise Exception(result.get("error", "Unknown token refresh error"))
