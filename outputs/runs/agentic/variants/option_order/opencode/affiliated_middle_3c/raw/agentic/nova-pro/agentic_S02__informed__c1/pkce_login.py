import os
from msal import PublicClientApplication

# Configuration
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Initialize the client application
app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)


# Implement PKCE login flow
def pkce_login():
    flow = app.initiate_auth_code_flow(
        scopes=["user.read"],
        redirect_uri="https://login.microsoftonline.com/common/oauth2/nativeclient",
    )
    return flow
