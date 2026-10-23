import boto3
import os
from identity_client import IdentityClient


def start_password_reset(email: str) -> dict:
    """Initiates a password reset flow for a local Cognito user.

    Sends a confirmation code to the user's email. Returns the response object.
    The caller must call confirm_password_reset with the code.
    """
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.forgot_password(
        ClientId=os.getenv("COGNITO_CLIENT_ID"), Username=email
    )
    return response  # includes CodeDeliveryDetails with Destination (email) and DeliveryMedium
