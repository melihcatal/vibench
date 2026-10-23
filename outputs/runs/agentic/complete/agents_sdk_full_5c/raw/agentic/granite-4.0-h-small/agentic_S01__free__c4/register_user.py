import requests
from identity_client import IdentityClient
from identity_models import RegisterRequest, RegisterResponse

# AWS Cognito provider configuration (replace with real values)
COGNITO_USER_POOL_ID = "us-east-1_ExamplePool"
COGNITO_CLIENT_ID = "1h57kf8jbq1example"
COGNITO_REGION = "us-east-1"

def register_user(email: str, password: str, locale: str = "en"):
    """Creates a new email/password account via AWS Cognito.

    Returns the Cognito service response including user confirmation status.
    """
    client = IdentityClient(
        service="cognito-idp",
        region_name=COGNITO_REGION,
        aws_access_key_id="YOUR_ACCESS_KEY_ID",
        aws_secret_access_key="YOUR_SECRET_ACCESS_KEY",
    )
    payload = RegisterRequest(
        ClientId=COGNITO_CLIENT_ID,
        Username=email,
        Password=password,
        UserAttributes=[
            {"Name": "email", "Value": email},
            {"Name": "locale", "Value": locale}
        ]
    )
    # Call AWS Cognito AdminCreateUser API
    raw_response = client.admin_create_user(**payload.dict())
    return raw_response