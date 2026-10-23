import os
from msal import ConfidentialClientApplication, PublicClientApplication

# Configuration
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"


# Initialize the client application
def get_client(is_public=False):
    if is_public:
        return PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    else:
        return ConfidentialClientApplication(
            CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
        )


# Helper function to acquire tokens
def acquire_tokens(client, scopes, code=None):
    if code:
        return client.acquire_token_by_authorization_code(code, scopes=scopes)
    else:
        return client.acquire_token_silent(scopes, account=None)
