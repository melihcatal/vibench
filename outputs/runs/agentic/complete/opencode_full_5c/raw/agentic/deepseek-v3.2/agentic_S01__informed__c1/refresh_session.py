import os
from identity_client import get_cognito_client
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_token: str) -> RefreshResponse:
    """Refresh an expired session or access token using Amazon Cognito."""
    client = get_cognito_client()

    try:
        response = client.initiate_auth(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": refresh_token},
        )

        auth_result = response.get("AuthenticationResult", {})

        return RefreshResponse(
            success=True,
            access_token=auth_result.get("AccessToken"),
            id_token=auth_result.get("IdToken"),
            expires_in=auth_result.get("ExpiresIn"),
            token_type=auth_result.get("TokenType"),
            message="Session refreshed successfully",
        )
    except client.exceptions.NotAuthorizedException:
        return RefreshResponse(
            success=False,
            access_token=None,
            id_token=None,
            expires_in=None,
            token_type=None,
            message="Invalid or expired refresh token",
        )
    except Exception as e:
        return RefreshResponse(
            success=False,
            access_token=None,
            id_token=None,
            expires_in=None,
            token_type=None,
            message=f"Refresh failed: {str(e)}",
        )
