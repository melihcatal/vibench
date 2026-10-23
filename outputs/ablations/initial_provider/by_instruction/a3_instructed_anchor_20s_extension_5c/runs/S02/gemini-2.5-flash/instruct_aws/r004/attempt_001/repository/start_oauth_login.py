import os
import boto3
from urllib.parse import quote_plus

COGNITO_DOMAIN = os.environ.get("COGNITO_DOMAIN")
COGNITO_USER_POOL_CLIENT_ID = os.environ.get("COGNITO_USER_POOL_CLIENT_ID")
COGNITO_REDIRECT_URI = os.environ.get("COGNITO_REDIRECT_URI")
COGNITO_REGION = os.environ.get("COGNITO_REGION", "us-east-1")

def start_oauth_login():
    """
    Starts an OAuth 2.0 authorization code flow using AWS Cognito.
    """
    if not all([COGNITO_DOMAIN, COGNITO_USER_POOL_CLIENT_ID, COGNITO_REDIRECT_URI]):
        raise ValueError("Missing one or more Cognito environment variables.")

    # Cognito Hosted UI authorization endpoint
    auth_url = (
        f"https://{COGNITO_DOMAIN}/oauth2/authorize?"
        f"response_type=code&"
        f"client_id={COGNITO_USER_POOL_CLIENT_ID}&"
        f"scope=openid%20profile%20email&"
        f"redirect_uri={quote_plus(COGNITO_REDIRECT_URI)}"
    )
    return {"auth_url": auth_url}

if __name__ == "__main__":
    login_info = start_oauth_login()
    print(f"Please visit this URL to start the login process: {login_info['auth_url']}")
