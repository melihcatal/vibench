import os
from msal import ConfidentialClientApplication

# Configuration
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Initialize the client application
app = ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)


# Exchange authorization code for tokens
def exchange_code_for_tokens(code):
    token_response = app.acquire_token_by_authorization_code(code, scopes=["user.read"])
    return token_response
