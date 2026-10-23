import requests
from identity_client import IdentityClient
from identity_models import PasswordResetRequest, PasswordResetResponse

# AWS Cognito config (replace with real values)
COGNITO_USER_POOL_ID = "us-east-1_ExamplePool"
COGNITO_CLIENT_ID = "1h57kf8jbq1example"
COGNITO_REGION = "us-east-1"

def password_reset(email: str):
    """Starts a password reset flow for a local email/password account via AWS Cognito.

    Returns a PasswordResetResponse indicating whether a reset confirmation code was sent.
    """
    client = IdentityClient(
        service="cognito-idp",
        region_name=COGNITO_REGION,
        aws_access_key_id="YOUR_ACCESS_KEY_ID",
        aws_secret_access_key="YOUR_SECRET_ACCESS_KEY",
    )
    payload = PasswordResetRequest(
        ClientId=COGNITO_CLIENT_ID,
        Username=email
    )
    raw = client.forgot_password(**payload.dict())
    return PasswordResetResponse(**raw)
