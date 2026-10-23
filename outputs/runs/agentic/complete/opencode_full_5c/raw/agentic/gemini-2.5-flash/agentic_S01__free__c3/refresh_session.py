import os
import boto3
from identity_models import RefreshSessionRequest, RefreshSessionResponse
from identity_client import (
    get_cognito_client,
    get_cognito_user_pool_id,
    get_cognito_client_id,
)


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    cognito_client = get_cognito_client()
    client_id = request.client_id

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
        raise ValueError("Refresh token is invalid or expired.")
    except Exception as e:
        raise RuntimeError(f"Cognito session refresh failed: {e}")


if __name__ == "__main__":
    # Example usage (requires environment variables to be set)
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["COGNITO_USER_POOL_ID"] = "YOUR_USER_POOL_ID"
    os.environ["COGNITO_CLIENT_ID"] = "YOUR_CLIENT_ID"
    # A valid refresh token is needed for this example to work
    # refresh_token = "YOUR_REFRESH_TOKEN"

    # try:
    #     refresh_request = RefreshSessionRequest(
    #         refresh_token=refresh_token,
    #         client_id=get_cognito_client_id(),
    #         user_pool_id=get_cognito_user_pool_id()
    #     )
    #     response = refresh_session(refresh_request)
    #     print(f"Session refreshed. New Access Token: {response.access_token[:10]}..., Expires in: {response.expires_in}s")
    # except Exception as e:
    #     print(f"Error during session refresh: {e}")
    print(
        "Please provide a valid refresh token and uncomment the example usage to run this script."
    )
