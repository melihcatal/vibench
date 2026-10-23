import os
import webbrowser
import urllib.parse
from identity_client import FederatedIdentityClient

def start_oauth_login(provider='cognito'):
    """Start an OAuth/OIDC authorization‑code login flow.
    Uses the selected provider's redirect endpoint and stores the state for later verification.
    """
    client = FederatedIdentityClient(provider=provider)
    # Build authorization URL
    auth_url = client.get_authorize_url(state='random_state')  # In production store/verify state
    print('Open the following URL in your browser:')
    print(auth_url)
    webbrowser.open(auth_url)

if __name__ == '__main__':
    # Example: start_oauth_login('cognito')
    start_oauth_login()
