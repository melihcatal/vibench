import os
import json
import urllib.parse
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Cognito Hosted UI Federation
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")


def build_login_url(redirect_uri, scope="openid email profile"):
    """Generate the Cognito OAuth authorization URL.
    Args:
        redirect_uri (str): The URL Cognito will redirect back to after login.
        scope (str): OAuth scopes to request.
    Returns:
        str: Fully formed authorization URL.
    """
    params = {
        "response_type": "code",
        "client_id": COGNITO_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "prompt": "consent",
    }
    query = urllib.parse.urlencode(params)
    login_url = (
        f"https://{COGNITO_DOMAIN}.auth.{COGNITO_DOMAIN}.amazoncognito.com/login?"
        + query
    )
    return login_url


def start_oauth_login(redirect_uri, scope="openid email profile"):
    """Start an OAuth 2.0 authorization code flow using Cognito Hosted UI.
    Args:
        redirect_uri (str): URL to receive the authorization code.
        scope (str): OAuth scopes to request.
    Returns:
        str: The authorization URL.
    """
    try:
        url = build_login_url(redirect_uri, scope)
    except Exception as e:
        raise RuntimeError(f"Failed to build Cognito login URL: {e}")
    return url


# Example usage:
# print(start_oauth_login('https://myapp.example.com/callback'))
