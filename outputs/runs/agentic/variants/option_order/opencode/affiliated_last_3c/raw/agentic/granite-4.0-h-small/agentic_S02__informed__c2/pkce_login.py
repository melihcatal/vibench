import msal
import os
from identity_client import IdentityClient


def pkce_login():
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    # MSAL ConfidentialClientApplication supports PKCE for public clients via PublicClientApplication
    client = msal.PublicClientApplication(client_id, authority=authority)
    # Build authorization URL with PKCE
    auth_url, state = client.get_authorization_request_url(
        ["profile openid"],
        redirect_uri="http://localhost:5000/callback",
        scopes=["profile openid"],
    )
    print("Open this URL in your browser:", auth_url)
    print(
        "After authorization, you will be redirected to the redirect URI with ?code=...&state=..."
    )
    # In a real app, capture the code and state via your web server's callback handler
    # Exchange code for token via acquire_token_by_code (PKCE flow handles verification internally)
    return auth_url


if __name__ == "__main__":
    start = pkce_login()
    if start:
        print("Start the flow by visiting:", start)
