import os
from botocore.exceptions import ClientError
from identity_client import get_cognito_client, COGNITO_CLIENT_ID
from identity_models import PasswordResetRequest

def initiate_password_reset(reset_request: PasswordResetRequest) -> dict:
    """
    Starts a password reset flow for a user with Amazon Cognito.
    """
    cognito_client = get_cognito_client()
    if not COGNITO_CLIENT_ID:
        raise ValueError("COGNITO_CLIENT_ID environment variable is not set.")

    try:
        response = cognito_client.forgot_password(
            ClientId=COGNITO_CLIENT_ID,
            Username=reset_request.email
        )
        return response['CodeDeliveryDetails']
    except ClientError as e:
        # Handle exceptions, e.g., UserNotFoundException
        print(f"Error initiating password reset: {e}")
        raise
