import os
from google.oauth2 import service_account

# Load the service account key file
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account-key.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Refresh the access token
credentials.refresh(requests.Request())

# Print the refreshed access token
print('Refreshed access token:', credentials.token)