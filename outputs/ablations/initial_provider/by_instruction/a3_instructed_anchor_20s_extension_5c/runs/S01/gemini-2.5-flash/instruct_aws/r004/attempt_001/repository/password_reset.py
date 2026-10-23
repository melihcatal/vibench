import boto3
from identity_models import PasswordResetRequest, PasswordResetResponse
from identity_client import IdentityClientConfig

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    client = boto3.client("cognito-idp", region_name=IdentityClientConfig.AWS_REGION)
    client.forgot_password(
        ClientId=IdentityClientConfig.COGNITO_CLIENT_ID,
        Username=request.email,
    )
    return PasswordResetResponse(message="Password reset initiated. Check your email.")
