import os
import requests
from requests.auth import HTTPBasicAuth

# Load Cognito credentials from environment
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")
USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")

# Initialize Boto3 SDK client for Cognito Identity Provider
client = boto3.client(
    "cognito-idp",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def email_password_login(email: str, password: str) -> dict:
    """Sign in user with email and password using Amazon Cognito User Pools.
    Returns tokens (access_token, id_token, refresh_token) on success.
    """
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=CLIENT_ID,
        AuthParameters={"USERNAME": email, "PASSWORD": password},
    )
    return response["AuthenticationResult"]
