from identity_client import FirebaseAuthClient
from identity_models import RefreshTokenRequest, AuthTokenResponse


def refresh_user_session(refresh_request: RefreshTokenRequest) -> AuthTokenResponse:
    """
    Refreshes an ID token using a refresh token via the Firebase Auth REST API.
    """
    client = FirebaseAuthClient()
    try:
        response_data = client.refresh_id_token(refresh_request.refresh_token)
        return AuthTokenResponse(
            id_token=response_data["id_token"],
            refresh_token=response_data["refresh_token"],
            expires_in=int(response_data["expires_in"]),
            local_id=response_data["local_id"],
        )
    except Exception as e:
        raise Exception(f"Token refresh failed: {str(e)}")
