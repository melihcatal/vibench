import boto3
from identity_models import RefreshSessionRequest, RefreshSessionResponse
from identity_client import IdentityClientConfig

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    client = boto3.client("cognito-idp", region_name=IdentityClientConfig.AWS_REGION)
    response = client.initiate_auth(
        ClientId=IdentityClientConfig.COGNITO_CLIENT_ID,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={
            "REFRESH_TOKEN": request.refresh_token,
        },
    )
    result = response["AuthenticationResult"]
    return RefreshSessionResponse(
        access_token=result["AccessToken"],
        id_token=result["IdToken"],
        expires_in=result["ExpiresIn"],
        token_type=result["TokenType"],
    )
