import os
from urllib.parse import urlencode
import secrets

from identity_client import IdentityClientConfig, build_authorization_url
from identity_models import AuthCodeRequest

def start_oauth_login_flow():
    # Generate a secure state parameter to prevent CSRF attacks
    state = secrets.token_urlsafe(32)

    # In a real application, you would store the state in the user's session
    # for verification during the callback.
    # For this example, we'll just print it.
    print(f"Generated State: {state}")

    auth_request = AuthCodeRequest(
        client_id=IdentityClientConfig.AZURE_AD_CLIENT_ID,
        redirect_uri=IdentityClientConfig.REDIRECT_URI,
        scope="openid profile email User.Read", # User.Read for Microsoft Graph
        response_type="code",
        state=state
    )

    authorization_url = build_authorization_url(
        client_id=auth_request.client_id,
        redirect_uri=auth_request.redirect_uri,
        scope=auth_request.scope,
        state=auth_request.state,
        response_type=auth_request.response_type,
    )

    print(f"Please navigate to the following URL to initiate login:\n{authorization_url}")
    return authorization_url

if __name__ == "__main__":
    # Example usage: Ensure environment variables are set for a real flow
    # os.environ["AZURE_AD_CLIENT_ID"] = "YOUR_AZURE_AD_CLIENT_ID"
    # os.environ["AZURE_AD_TENANT_ID"] = "YOUR_AZURE_AD_TENANT_ID" # or "common"
    # os.environ["REDIRECT_URI"] = "http://localhost:8000/oauth/callback"
    start_oauth_login_flow()
