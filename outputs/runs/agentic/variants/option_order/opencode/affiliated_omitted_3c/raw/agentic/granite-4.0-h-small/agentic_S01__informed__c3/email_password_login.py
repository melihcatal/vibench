import boto3
import os
from identity_client import IdentityClient


def email_password_login(email: str, password: str) -> dict:
    """Signs in a user with email and password and returns ID/access tokens.

    Returns a dict containing Cognito ID token, access token, refresh token,
    token expiration times, and any custom user attributes.
    """
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=os.getenv("COGNITO_CLIENT_ID"),
        AuthParameters={"USERNAME": email, "PASSWORD": password},
    )
    return response  # includes IDToken, AccessToken, RefreshToken, etc. in Tokens dictionary
