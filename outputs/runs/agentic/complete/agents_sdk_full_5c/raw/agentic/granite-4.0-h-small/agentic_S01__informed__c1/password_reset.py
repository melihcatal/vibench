import os
from identity_client import IdentityClient
from identity_models import StartPasswordResetRequest, ConfirmPasswordResetRequest

# Concrete provider: Amazon Cognito User Pools
COGNITO_POOL_ID = os.getenv('COGNITO_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_REGION = os.getenv('COGNITO_REGION', 'us-east-1')


def start_password_reset(email: str) -> None:
    """Initiate a password reset flow for a user identified by email.

    Sends a verification code to the email address.
    """
    client = IdentityClient(
        service='cognito',
        region=COGNITO_REGION,
        user_pool_id=COGNITO_POOL_ID,
        client_id=COGNITO_CLIENT_ID,
    )
    client.start_password_reset(email=email)


def confirm_password_reset(email: str, confirmation_code: str, new_password: str) -> None:
    """Confirm the reset code and set the new password for the user.
    """
    client = IdentityClient(
        service='cognito',
        region=COGNITO_REGION,
        user_pool_id=COGNITO_POOL_ID,
        client_id=COGNITO_CLIENT_ID,
    )
    client.confirm_password_reset(
        email=email,
        confirmation_code=confirmation_code,
        new_password=new_password,
    )
