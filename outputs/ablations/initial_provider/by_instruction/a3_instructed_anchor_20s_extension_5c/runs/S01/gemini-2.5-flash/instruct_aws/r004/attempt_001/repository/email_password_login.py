import boto3
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse
from identity_client import IdentityClientConfig

def email_password_login(request: EmailPasswordLoginRequest) -> EmailPasswordLoginResponse:
    client = boto3.client("cognito-idp", region_name=IdentityClientConfig.AWS_REGION)
    response = client.initiate_auth(
        ClientId=IdentityClientConfig.COGNITO_CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": request.email,
            "PASSWORD": request.password,
        },
    )
    result = response["AuthenticationResult"]
    return EmailPasswordLoginResponse(
        access_token=result["AccessToken"],
        refresh_token=result["RefreshToken"],
        id_token=result["IdToken"],
        expires_in=result["ExpiresIn"],
        token_type=result["TokenType"],
    )
