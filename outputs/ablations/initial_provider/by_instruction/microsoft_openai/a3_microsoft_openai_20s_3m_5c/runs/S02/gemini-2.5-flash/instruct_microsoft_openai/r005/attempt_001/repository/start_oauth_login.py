import os
import uuid
from urllib.parse import urlencode

from identity_client import IdentityClient
from identity_models import OAuthState

def start_oauth_login(redirect_uri: str) -> str:
    """Starts an OAuth authorization-code login flow with Azure AD.

    Args:
        redirect_uri: The URI where the authorization code will be sent.

    Returns:
        The URL to redirect the user for login.
    """
    client = IdentityClient()
    session_id = str(uuid.uuid4())
    
    # In a real application, you would store this state in a session or database
    # along with the session_id to verify it in the callback.
    oauth_state = OAuthState(session_id=session_id, redirect_uri=redirect_uri)
    # For simplicity, we are just using the session_id as the state parameter directly
    # A robust solution would serialize and sign the OAuthState object.

    authorization_url = client.get_authorization_url(redirect_uri, oauth_state.session_id)
    return authorization_url

if __name__ == '__main__':
    # Example usage (replace with your actual redirect URI)
    # Make sure to set AZURE_AD_TENANT_ID, AZURE_AD_CLIENT_ID environment variables
    login_url = start_oauth_login("http://localhost:8000/oauth_callback")
    print(f"Please visit this URL to log in: {login_url}")
