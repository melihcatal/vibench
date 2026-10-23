import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.cloud import identity

# Configuration
PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')
SERVICE_ACCOUNT_KEY_PATH = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY_PATH')

# Initialize client
def get_identity_client():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_KEY_PATH,
        scopes=['https://www.googleapis.com/auth/cloud-identity.readonly']
    )
    return identity.IdentityServiceClient(credentials=credentials)