import requests
from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse

# AWS Cognito credentials (replace with real values)
COGNITO_USER_POOL_ID = "us-east-1_ExamplePool"
COGNITO_CLIENT_ID = "1h57kf8jbq1example"
COGNITO_REGION = "us-east-1"

def email_password_login(email: str, password: str):
    """Signs in with email/password via AWS Cognito and returns tokens.

    Returns an instance of LoginResponse containing id_token, access_token,
    refresh_token, and token expiration data.
    """
    client = IdentityClient(
        service="cognito-idp",
        region_name=COGNITO_REGION,
        aws_access_key_id="YOUR_ACCESS_KEY_ID",
        aws_secret_access_key="YOUR_SECRET_ACCESS_KEY",
    )
    payload = LoginRequest(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": email, "PASSWORD": password},
        UserPoolId=COGNITO_USER_POOL_ID
    )
    # AWS SDK method for user authentication
    raw = client.initiate_auth(**payload.dict())
    return LoginResponse(**raw)
