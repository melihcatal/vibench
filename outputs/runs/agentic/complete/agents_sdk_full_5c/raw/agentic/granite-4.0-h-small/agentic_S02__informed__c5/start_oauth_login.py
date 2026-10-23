import os
import webbrowser
import requests
from identity_client import IdentityClient

def start_oauth_login():
    # Auth0 configuration (can be swapped for other providers)
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'YOUR_AUTH0_DOMAIN')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID', 'YOUR_AUTH0_CLIENT_ID')
    REDIRECT_URI = 'http://localhost:8000/oauth_callback'
    SCOPE = 'openid profile email'

    # Build authorization URL
    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"response_type=code&"
        f"client_id={AUTH0_CLIENT_ID}&"
        f"redirect_uri={requests.utils.quote(REDIRECT_URI)}&"
        f"scope={requests.utils.quote(SCOPE)}&"
        f"connection=USERNAME-PASSWORD-AUTHENTICATION"
    )

    print(f"Go to this URL to login: {auth_url}")
    webbrowser.open(auth_url)

if __name__ == '__main__':
    start_oauth_login()
