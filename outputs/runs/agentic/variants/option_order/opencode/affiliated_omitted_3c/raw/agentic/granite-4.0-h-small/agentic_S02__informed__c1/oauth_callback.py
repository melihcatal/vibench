import os
import urllib.parse
import requests
from requests.exceptions import RequestException

# Microsoft identity platform token endpoint
TOKEN_ENDPOINT = "https://login.microsoftonline.com/{}/token".format(
    os.getenv("AZURE_TENANT_ID")
)
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")


def exchange_code_for_tokens(code, redirect_uri):
    """Exchange an authorization code for access and ID tokens using MSAL SDK.
    Args:
        code (str): Authorization code from the callback.
        redirect_uri (str): The redirect URI registered in Azure AD.
    Returns:
        dict: Parsed JSON response with access_token, id_token, refresh_token, etc.
    """
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "openid email profile",
    }
    try:
        response = requests.post(TOKEN_ENDPOINT, data=data)
        response.raise_for_status()
    except RequestException as e:
        raise RuntimeError(f"Token exchange failed: {e}")
    return response.json()


# Example (for local testing):
# tokens = exchange_code_for_tokens(auth_code, 'https://myapp.com/callback')
# print(tokens)
