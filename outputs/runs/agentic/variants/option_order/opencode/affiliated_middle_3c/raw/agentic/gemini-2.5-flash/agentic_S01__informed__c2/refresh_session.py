from identity_client import Auth0AuthenticationClient
from identity_models import RefreshTokenRequest, RefreshTokenResponse


def refresh_session(request: RefreshTokenRequest) -> RefreshTokenResponse:
    client = Auth0AuthenticationClient()
    response = client.post(
        "oauth/token",
        {
            "client_id": client.client_id,
            "refresh_token": request.refresh_token,
            "grant_type": request.grant_type,
            "scope": request.scope,
        },
    )
    response.raise_for_status()
    data = response.json()
    return RefreshTokenResponse(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        token_type=data["token_type"],
        expires_in=data["expires_in"],
    )
