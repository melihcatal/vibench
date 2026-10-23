import os
import sys
import boto3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from identity_client import IdentityClient
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    identity_client = IdentityClient()
    cognito_client = identity_client.get_cognito_idp_client()
    client_id = identity_client.get_client_id()

    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": request.refresh_token},
        )

        auth_result = response["AuthenticationResult"]
        return RefreshSessionResponse(
            access_token=auth_result["AccessToken"],
            id_token=auth_result["IdToken"],
            expires_in=auth_result["ExpiresIn"],
        )
    except cognito_client.exceptions.NotAuthorizedException:
        return RefreshSessionResponse(
            access_token="", id_token="", expires_in=0, message="Invalid refresh token."
        )
    except Exception as e:
        return RefreshSessionResponse(
            access_token="",
            id_token="",
            expires_in=0,
            message=f"Refresh session failed: {str(e)}",
        )
