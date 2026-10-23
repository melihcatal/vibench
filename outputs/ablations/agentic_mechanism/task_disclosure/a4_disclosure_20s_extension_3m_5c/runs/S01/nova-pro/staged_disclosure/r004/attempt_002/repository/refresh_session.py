import os
import requests
from google.oauth2 import service_account

# Load the service account credentials
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account.json',
    scopes=['https://www.googleapis.com/auth/userinfo.email']
)

# Refresh the access token
def refresh_session():
    if credentials.expired:
        credentials.refresh(requests)
        print('Session refreshed successfully!')
    else:
        print('Session is still valid.')

# Example usage
refresh_session()