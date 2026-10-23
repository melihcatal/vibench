import msal
import os
from identity_client import IdentityClient


def start_oauth_login():
    # Microsoft Entra OIDC configuration
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    # Initialize MSAL client with client credentials flow (authorization code grant)
    client = msal.ConfidentialClientApplication(client_id, authority=authority)
    # Build the authorization URL for the login
    auth_url = client.get_authorization_request_url(
        ["profile", "openid"], scope="user.read"
    )
    print("Open this URL in a browser to complete login:", auth_url)
    return auth_url


if __name__ == "__main__":
    start_oauth_login()
