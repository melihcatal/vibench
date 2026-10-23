import os
from identity_client import get_identity_client
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_session(refresh_token: str) -> RefreshSessionResponse:
    client = get_identity_client()
    
    response = client.initiate_auth(
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={
            "REFRESH_TOKEN": refresh_token
        },
        ClientId=os.getenv("AWS_COGNITO_CLIENT_ID")
    )
    
    return RefreshSessionResponse(
        access_token=response["AuthenticationResult"]["AccessToken"],
        id_token=response["AuthenticationResult"]["IdToken"],
        expires_in=response["AuthenticationResult"]["ExpiresIn"]
    )