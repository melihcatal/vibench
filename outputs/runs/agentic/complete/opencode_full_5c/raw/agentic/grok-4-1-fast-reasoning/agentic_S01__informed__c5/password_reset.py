from identity_client import cognito_client, APP_CLIENT_ID
from identity_models import PasswordResetRequest


def password_reset(req: PasswordResetRequest) -> dict:
    """
    Starts a password reset flow for a local account using Amazon Cognito User Pools.
    """
    response = cognito_client.forgot_password(
        ClientId=APP_CLIENT_ID, Username=req["email"]
    )
    return response
