import boto3
import os
from identity_client import IdentityClient


def register_user(email: str, password: str) -> dict:
    """Creates a new email/password user account using Amazon Cognito User Pools.

    Returns a dict with the new user's attributes and confirmation status.
    """
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.sign_up(
        ClientId=os.getenv("COGNITO_CLIENT_ID"),
        Username=email,
        Password=password,
        UserAttributes=[{"Name": "email", "Value": email}],
    )
    # Optional: confirm registration if auto-verification is disabled
    # client.admin_confirm_sign_up(UserPoolId=os.getenv('COGNITO_POOL_ID'), Username=email)
    return response
